def pl_translation(data: dict):
    """Translate data provided by DatesParser class."""
    if not data:
        return 'Teraz.'

    event_time_iso = data["event_time"].isoformat(timespec="minutes")
    weekdays = {
        0: 'poniedziałek',
        1: 'wtorek',
        2: 'środę',
        3: 'czwartek',
        4: 'piątek',
        5: 'sobotę',
        6: 'niedzielę'
    }

    result = []
    # Check if years:
    if data['years']:
        if data["years"] == 1:
            result.append('rok')
        elif data["years"] % 10 in (2, 3, 4) and data["years"] not in (12, 13, 14):
            result.append(f'{data["years"]} lata')
        else:
            result.append(f'{data["years"]} lat')

    # Check if months:
    if data["months"]:
        if data["months"] == 1:
            result.append('miesiąc')
        elif data["months"] in (2, 3, 4):
            result.append(f'{data["months"]} miesiące')
        else:
            result.append(f'{data["months"]} miesięcy')

    # Check if result should be special depending on weekdays:
    if not result:
        if data["weekday"] is not None and data["days"] > 1:
            if data["is_event_in_the_future"]:
                return f'W przyszł{"ą" if data["weekday"] in (2, 5, 6) else "y"} {weekdays[data["weekday"]]} ' \
                       f'o {event_time_iso}.'
            else:
                return f'W zeszł{"ą" if data["weekday"] in (2, 5, 6) else "y"} {weekdays[data["weekday"]]} ' \
                       f'o {event_time_iso}.'

        # Use weeks only if it's a first value in returned string.
        else:
            data["weeks"] = data["days"] // 7
            data["days"] = data["days"] % 7
            if data["weeks"]:
                if data["weeks"] == 1:
                    result.append('tydzień')
                else:
                    result.append(f'{data["weeks"]} tygodnie')

    # Check if days-delta is in 2-day range...
    if not result and data["days_delta"]:
        if data["days_delta"] == 2:
            return (f'Pojutrze' if data["is_event_in_the_future"] else 'Przedwczoraj') + f' o {event_time_iso}.'
        # ...additional case when event just ended or it's about to begin shortly.
        if data["days_delta"] == 1 and data["hours"] >= 3:
            return (f'Jutro' if data["is_event_in_the_future"] else 'wczoraj') + f' o {event_time_iso}.'

    # Check if days:
    if data["days"]:
        result.append('dzień' if data["days"] == 1 else f'{data["days"]} dni')

    # Check if hours:
    if data["hours"]:
        if data["hours"] == 1:
            result.append('godzinę')
        elif data["hours"] in (2, 3, 4, 22, 23):
            result.append(f'{data["hours"]} godziny')
        else:
            result.append(f'{data["hours"]} godzin')

    # Check if minutes, add only if event is in range of a couple of days.
    if data["minutes"] and (data["years"] + data["months"] + data["weeks"]) == 0:
        if data["minutes"] == 1:
            result.append('minutę')
        elif data["minutes"] % 10 in (2, 3, 4) and data["minutes"] not in (12, 13, 14):
            result.append(f'{data["minutes"]} minuty')
        else:
            result.append(f'{data["minutes"]} minut')

    # Check if result:
    if result:
        result = f'{", ".join(result[:-1])} i {result[-1]}' if len(result) > 1 else f'{result[0]}'
        if data["is_event_in_the_future"]:
            return f'Za {result}.'
        else:
            return f'{result.capitalize()} temu.'

    # Extreme case if only delta is the one in seconds:
    else:
        return 'Za niecałą minutę.' if data["is_event_in_the_future"] else 'Niecałą minutę temu.'
