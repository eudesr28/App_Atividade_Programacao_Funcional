from datetime import datetime, timedelta

def filter_hours(generator, condition):
    return [h for h in generator if condition(h)]

def generate_hours(start="08:00", end="18:00", interval=60): 
    """
    Gera uma lista de horários entre 'start' e 'end' com intervalo em minutos.
    Exemplo: generate_hours("08:00", "12:00", 60) -> ['08:00', '09:00', '10:00', '11:00']
    """
    start_time = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")
    delta = timedelta(minutes=interval)

    return [
        (start_time + i * delta).strftime("%H:%M")
        for i in range(int((end_time - start_time) / delta))
    ]
