import json
import socket
import socketserver
import threading
import time

import conexion_artnet
import globales

TIMEOUT = 10
HOST = 'localhost'
PORT = 8081


def detenerTheadsViejos():
    globales.REPETICION = False
    time.sleep(2)
    globales.REPETICION = True


# ----------------------------------------------------- SERVIDOR ----------------------------------------------------- #


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            threadName = threading.currentThread().getName()
            activeThreads = threading.activeCount() - 1
            clientIP = self.client_address[0]
            print('[%s] -- New connection from %s -- Active threads: %d' % (threadName, clientIP, activeThreads))
            data = self.request.recv(1024).strip()
            dataJson = json.loads(data.decode('utf8'))
            self.request.sendall(data)

            print("{} wrote:".format(self.client_address[0]))
            print(dataJson)

            # CREAR LISTA Y VERIFICAR SI EXISTE EL DISPOSITIVO

            artnet = conexion_artnet.ConexionArtnet()
            artnet.dispositivosActivos.clear()
            accion = dataJson['accion']
            dispositivosActuales = dataJson['lista']
            numeroDispositivos = int(len(dispositivosActuales) / 6)

            for repeticion in range(numeroDispositivos):
                numero = repeticion * 7

                ip = dispositivosActuales[numero]
                universo = int(dispositivosActuales[numero + 1])
                matrizX = int(dispositivosActuales[numero + 2])
                matrizY = int(dispositivosActuales[numero + 3])
                patch = dispositivosActuales[numero + 4]
                orden = dispositivosActuales[numero + 5]
                tipoLed = dispositivosActuales[numero + 6]

                if orden == 'Arriba-Izquierda':
                    orden = 0
                elif orden == 'Arriba':
                    orden = 1
                elif orden == 'Arriba-Derecha':
                    orden = 2
                elif orden == 'Izquierda':
                    orden = 3
                elif orden == 'Centro':
                    orden = 4
                elif orden == 'Derecha':
                    orden = 5
                elif orden == 'Abajo-Izquierda':
                    orden = 6
                elif orden == 'Abajo':
                    orden = 7
                elif orden == 'Abajo-Derecha':
                    orden = 8

                artnet.buscarOAgregarDispositivo(ip, universo, patch, matrizX, matrizY, orden, tipoLed)

            artnet.dispositivosActivos = sorted(artnet.dispositivosActivos, key=lambda dispositivo: dispositivo.orden)

            artnet.printCantidadDispositivosActivos()
            artnet.printDispositivosActivos()

            if accion == 'probar':
                detenerTheadsViejos()
                artnet.probarDispositivo()

            if accion == 'color':
                detenerTheadsViejos()
                artnet.color(dataJson)

            if accion == 'scroll':
                t1 = threading.Thread(target=artnet.scroll, args=(dataJson,), daemon=True)
                detenerTheadsViejos()
                t1.start()
                t1.join()

            if accion == 'scan':
                t2 = threading.Thread(target=artnet.scan, args=(dataJson,), daemon=True)
                detenerTheadsViejos()
                t2.start()
                t2.join()

            if accion == 'estrellas':
                t3 = threading.Thread(target=artnet.estrellas, args=(dataJson,), daemon=True)
                detenerTheadsViejos()
                t3.start()
                t3.join()

        except ValueError:
            msg = "<html><body><h1>This is a test</h1><p>More content here</p></body></html>"

            response_headers = {
                'Content-Type': 'text/html; encoding=utf8',
                'Content-Length': len(msg),
                'Connection': 'close',
            }

            response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.items())

            response_proto = 'HTTP/1.1'
            response_status = '200'
            response_status_text = 'OK'  # this can be random

            # sending all this stuff
            r = '%s %s %s\r\n' % (response_proto, response_status, response_status_text)
            self.request.sendall(bytes(r + response_headers_raw + '\r\n' + msg, "utf-8"))

            print('Datos sin JSON')

        except KeyboardInterrupt:
            print('[%s] -- %s -- Timeout on data transmission ocurred after %d seconds.' % (
                threadName, clientIP, TIMEOUT))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def finish_request(self, request, client_address):
        request.settimeout(TIMEOUT)
        socketserver.TCPServer.finish_request(self, request, client_address)
        socketserver.TCPServer.close_request(self, request)


try:
    print("Starting server TCP at IP %s and port %d..." % (HOST, PORT))
    server = ThreadedTCPServer((HOST, PORT), RequestHandler)
    server.serve_forever()
except KeyboardInterrupt:
    server.socket.close()
