import datetime

def generar_turnos(h_apertura, h_cierre):
    apertura = datetime.datetime.strptime(
        h_apertura.strftime('%H:%M'), '%H:%M')
    cierre = datetime.datetime.strptime(h_cierre.strftime('%H:%M'), '%H:%M')
    turnos = []
    while(apertura < cierre):
        turnos.append(apertura.time())
        apertura = apertura + datetime.timedelta(minutes=30)
    return turnos
