import time
import DeviceClasses


class Parser:

    def __init__(self):

        self.a = DeviceClasses.Accel_Gyro()
        self.g = DeviceClasses.Accel_Gyro()
        self.a2 = DeviceClasses.Accel_Gyro()
        self.g2 = DeviceClasses.Accel_Gyro()
        self.speed = DeviceClasses.Speed()
        self.steer = DeviceClasses.Steer()
        self.pedals = DeviceClasses.Pedals()
        self.ecu = DeviceClasses.ECU()
        self.steeringWheel = DeviceClasses.SteeringWheel()
        self.cmds = DeviceClasses.Commands()
        self.invl = DeviceClasses.Inverter()
        self.invr = DeviceClasses.Inverter()
        self.bmsLV = DeviceClasses.BMS()
        self.bmsHV = DeviceClasses.BMS()
        self.gps = DeviceClasses.GPS()

        self.sensors = []

        self.cmds.time = time.time()

        self.a.type = "Accel"
        self.g.type = "Gyro"
        self.a2.type = "Accel IZZE"
        self.g2.type = "Gyro IZZE"
        self.invl.type = "Inverter Left"
        self.invr.type = "Inverter Right"
        self.bmsLV.type = "BMS LV"
        self.bmsHV.type = "BMS HV"

        self.sensors.append(self.ecu)
        self.sensors.append(self.steeringWheel)
        self.sensors.append(self.cmds)
        self.sensors.append(self.a)
        self.sensors.append(self.g)
        self.sensors.append(self.a2)
        self.sensors.append(self.g2)
        self.sensors.append(self.speed)
        self.sensors.append(self.steer)
        self.sensors.append(self.pedals)
        self.sensors.append(self.invl)
        self.sensors.append(self.invr)
        self.sensors.append(self.bmsLV)
        self.sensors.append(self.bmsHV)
        self.sensors.append(self.gps)

    def parseMessage(self, timestamp, id, msg):
        modifiedSensors = []

        if(id == 0xB0):
            # PEDALS
            if(msg[0] == 0x01):
                self.pedals.throttle1 = msg[1]
                self.pedals.throttle2 = msg[2]
                self.pedals.time = time.time()
                self.pedals.count += 1
                modifiedSensors.append(self.pedals.type)
                self.pedals.time = timestamp
            if(msg[0] == 0x02):
                self.pedals.brake = msg[1]
                self.pedals.front = (msg[2] * 256 + msg[4]) / 500
                self.pedals.back = (msg[5] * 256 + msg[7]) / 500

                # this next conversion is a correction of a wrong
                # computation before sending the value

                self.pedals.front = (
                    (((self.pedals.front/100)*4096)+0-409.6)/3276.8) * 100

                self.pedals.back = (
                    (((self.pedals.back/100)*4096)+0-409.6)/3276.8) * 100

                self.pedals.time = time.time()
                self.pedals.count += 1
                modifiedSensors.append(self.pedals.type)
                self.pedals.time = timestamp

        if(id == 0x4ED):
            self.a2.scale = 8
            self.a2.x = (msg[0] * 256 + msg[1])
            self.a2.y = (msg[2] * 256 + msg[3])
            self.a2.z = (msg[4] * 256 + msg[5])

            if(self.a2.x > 32768):
                self.a2.x -= 65536
            if(self.a2.y > 32768):
                self.a2.y -= 65536
            if(self.a2.z > 32768):
                self.a2.z -= 65536

            self.a2.x /= 100
            self.a2.y /= 100
            self.a2.z /= 100

            self.a2.x = round(self.a2.x, 2)
            self.a2.y = round(self.a2.y, 2)
            self.a2.z = round(self.a2.z, 2)

            self.a2.time = timestamp
            self.a2.count += 1
            modifiedSensors.append(self.a2.type)

        if(id == 0x4EC):
            self.g2.scale = 245
            self.g2.x = (msg[0] * 256 + msg[1])
            self.g2.y = (msg[2] * 256 + msg[3])
            self.g2.z = (msg[4] * 256 + msg[5])

            if(self.g2.x > 32768):
                self.g2.x -= 65536
            if(self.g2.y > 32768):
                self.g2.y -= 65536
            if(self.g2.z > 32768):
                self.g2.z -= 65536

            self.g2.x /= 100
            self.g2.y /= 100
            self.g2.z /= 100

            self.g2.x = round(self.g2.x, 2)
            self.g2.y = round(self.g2.y, 2)
            self.g2.z = round(self.g2.z, 2)

            self.g2.time = timestamp
            self.g2.count += 1
            modifiedSensors.append(self.g2.type)

        if(id == 0xC0):
            # ACCEL
            if(msg[0] == 0):
                self.a.scale = msg[7]
                self.a.x = (msg[1] * 256 + msg[2])/100 - self.a.scale
                self.a.y = (msg[3] * 256 + msg[4])/100 - self.a.scale
                self.a.z = (msg[5] * 256 + msg[6])/100 - self.a.scale

                self.a.x = round(self.a.x, 3)
                self.a.y = round(self.a.y, 3)
                self.a.z = round(self.a.z, 3)

                self.a.time = timestamp
                self.a.count += 1
                modifiedSensors.append(self.a.type)
            # GYRO
            if(msg[0] == 1):
                self.g.scale = msg[7]*10
                self.g.x = (msg[1] * 256 + msg[2])/10 - self.g.scale
                self.g.y = (msg[3] * 256 + msg[4])/10 - self.g.scale
                self.g.z = (msg[5] * 256 + msg[6])/10 - self.g.scale

                self.g.x = round(self.g.x, 3)
                self.g.y = round(self.g.y, 3)
                self.g.z = round(self.g.z, 3)

                self.g.time = timestamp
                self.g.count += 1
                modifiedSensors.append(self.g.type)

            # STEER
            if(msg[0] == 2):
                self.steer.angle = (msg[1] * 256 + msg[2])/100
                self.steer.angle = round(self.steer.angle, 3)
                self.steer.time = timestamp
                self.steer.count += 1
                modifiedSensors.append(self.steer.type)

        if(id == 0xD0):
            # SPEED
            if(msg[0] == 6):
                self.speed.l_enc = msg[1] * 256 + msg[2]
                self.speed.time = timestamp
                self.speed.count += 1
                modifiedSensors.append(self.speed.type)

            if(msg[0] == 7):
                self.speed.l_rads = (
                    (msg[1] << 16) + (msg[2] << 8) + msg[3]) / 10000
                if msg[7] == 1:
                    self.speed.l_rads *= -1

                self.speed.time = timestamp
                self.speed.count += 1
                modifiedSensors.append(self.speed.type)

            if(msg[0] == 0x015):
                self.speed.angle0 = (msg[1] * 256 + msg[2]) / 100
                self.speed.angle1 = (msg[3] * 256 + msg[4]) / 100
                self.speed.delta = (msg[5] * 256 + msg[6]) / 100
                self.speed.frequency = msg[7]
                self.speed.count += 1
                self.speed.time = timestamp
                modifiedSensors.append(self.speed.type)

        # ECU
        if(id == 0x55):
            # ECU State
            if(msg[0] == 0x10):
                self.ecu.state = msg[1]
                modifiedSensors.append(self.ecu.type)

            # ECU bms on request
            if(msg[0] == 0x0A):
                self.cmds.active_commands.append(
                    ("ECU BMS ON request", timestamp)
                )
                modifiedSensors.append(self.cmds.type)

            self.ecu.count += 1

        # STEERING
        if(id == 0xA0):
            if(msg[0] == 0x02):
                if(msg[1] == 0xEC):
                    self.ecu.map = -20
                else:
                    self.ecu.map = msg[1]
            if(msg[0] == 0x03):
                self.cmds.active_commands.append(
                    ("Steering Setup request", timestamp)
                )

            if(msg[0] == 0x04):
                self.cmds.active_commands.append(
                    ("Steering Stop request", timestamp)
                )

            if(msg[0] == 0x05):
                self.cmds.active_commands.append(
                    ("Steering RUN request", timestamp)
                )
                if(msg[1] == 0xEC):
                    self.ecu.map = -20
                else:
                    self.ecu.map = msg[1]

            self.steeringWheel.count += 1
            self.steeringWheel.time = timestamp
            modifiedSensors.append(self.steeringWheel.type)

        if(id == 0x201):
            if(msg[0] == 0x51 and msg[1] == 0x08):
                self.cmds.active_commands.append(
                    ("Inverter L ON", timestamp)
                )
                modifiedSensors.append(self.cmds.type)

        if(id == 0x202):
            if(msg[0] == 0x51 and msg[1] == 0x08):
                self.cmds.active_commands.append(
                    ("Inverter R ON", timestamp)
                )
                modifiedSensors.append(self.cmds.type)

        # BMS HV
        if(id == 0xAA):
            if(msg[0] == 0x01):
                self.bmsHV.voltage = ((msg[1] << 16) + (msg[2] << 8))/10000
                self.bmsHV.time = timestamp
                modifiedSensors.append(self.bmsHV.type)

            if(msg[0] == 0x05):
                self.bmsHV.current = (msg[1] * 256 + msg[2])/10
                self.bmsHV.time = timestamp
                modifiedSensors.append(self.bmsHV.type)

            if(msg[0] == 0xA0):
                self.bmsHV.temperature = (msg[1] * 256 + msg[2]) / 10

                self.bmsHV.time = timestamp
                self.bmsHV.count += 1
                modifiedSensors.append(self.bmsHV)

            if(msg[0] == 0x03):
                self.cmds.active_commands.append(
                    ("BMS is ON", timestamp)
                )
                modifiedSensors.append(self.cmds.type)
            if(msg[0] == 0x04):
                self.cmds.active_commands.append(
                    ("BMS is OFF", timestamp)
                )
                modifiedSensors.append(self.cmds.type)
            if(msg[0] == 0x08):
                self.cmds.active_commands.append(
                    ("BMS is OFF", timestamp)
                )
                modifiedSensors.append(self.cmds.type)

            self.bmsHV.count += 1

        if(id == 0xFF):
            self.bmsLV.voltage = msg[0]/10
            self.bmsLV.temperature = msg[2]/5
            self.bmsLV.count += 1
            self.bmsLV.time = timestamp
            modifiedSensors.append(self.bmsLV.type)

        # INVERTER LEFT
        if(id == 0x181):
            if(msg[0] == 0xA0):
                self.invl.torque = (msg[2] * 256 + msg[1])
                if(self.invl.torque > 32768):
                    self.invl.torque -= 65536
                self.invl.time = timestamp
            if(msg[0] == 0x4A):
                self.invl.temperature = (
                    msg[2] * 256 + msg[1] - 15797) / 112.1182
                self.invl.time = timestamp
            if(msg[0] == 0x49):
                self.invl.motorTemp = (msg[2] * 256 + msg[1] - 9393.9) / 55.1
                self.invl.time = timestamp
            if(msg[0] == 0xA8):
                self.invl.speed = (msg[2] * 256 + msg[1])
                if(self.invl.speed > 32768):
                    self.invl.speed -= 65536
                self.invl.time = timestamp

            self.invl.count += 1
            modifiedSensors.append(self.invl.type)

        # INVERTER RIGHT
        if(id == 0x182):
            if(msg[0] == 0xA0):
                self.invr.torque = (msg[2] * 256 + msg[1])
                if(self.invr.torque > 32768):
                    self.invr.torque -= 65536
                self.invr.time = timestamp
            if(msg[0] == 0x4A):
                self.invr.temperature = (
                    msg[2] * 256 + msg[1] - 15797) / 112.1182
                self.invr.time = timestamp
            if(msg[0] == 0x49):
                self.invr.motorTemp = (msg[2] * 256 + msg[1] - 9393.9) / 55.1
                self.invr.time = timestamp
            if(msg[0] == 0xA8):
                self.invr.speed = (msg[2] * 256 + msg[1])
                if(self.invr.speed > 32768):
                    self.invr.speed -= 65536
                self.invr.time = timestamp

            self.invr.count += 1
            modifiedSensors.append(self.invr.type)

        return modifiedSensors

    def parseCSV(self, timestamp, id, msg):
        modifiedSensors = []

        if(id == "/imu_old/accel"):
            a.scale = msg[3]
            a.scale = 4
            if(abs(msg[0]) > a.scale or abs(msg[1]) > a.scale or abs(msg[2]) > a.scale):
                return
            a.x = msg[0]
            a.y = msg[1]
            a.z = msg[2]
            a.count += 1
            a.time = timestamp
            modifiedSensors.append(a.type)

        if(id == "/imu_old/gyro"):
            g.scale = msg[3]
            if(abs(msg[0]) > g.scale or abs(msg[1]) > g.scale or abs(msg[2]) > g.scale):
                return
            g.x = msg[0]
            g.y = msg[1]
            g.z = msg[2]
            g.count += 1
            g.time = timestamp
            modifiedSensors.append(g.type)

        if(id == "/bms_lv/values"):
            bmsLV.voltage = msg[0]
            bmsLV.temp = msg[1]
            bmsLV.count += 1
            bmsLV.time = timestamp
            modifiedSensors.append(bmsLV.type)

        if(id == "/front_wheels_encoders/right/angle"):
            speed.count += 1
            modifiedSensors.append(speed.type)
            pass
        if(id == "/front_wheels_encoders/right/speed"):
            speed.r_kmh = msg[0]
            modifiedSensors.append(speed.type)
            speed.count += 1
        if(id == "/front_wheels_encoders/right/speed_rads"):
            speed.r_rads = msg[0]
            modifiedSensors.append(speed.type)
            speed.count += 1

        if(id == "/front_wheels_encoders/left/angle"):
            speed.count += 1
            modifiedSensors.append(speed.type)
            pass
        if(id == "/front_wheels_encoders/left/speed"):
            speed.count += 1
            modifiedSensors.append(speed.type)
            speed.l_kmh = msg[0]
        if(id == "/front_wheels_encoders/left/speed_rads"):
            speed.l_rads = msg[0]
            modifiedSensors.append(speed.type)
            speed.count += 1

    def fill_GPS(self, timestamp, type, payload):
        modified = False
        time_ = timestamp

        if(self.__count_empty_elements(payload) > 3):
            return modified

        self.gps.clear()

        if("GGA" in type):

            self.gps.timestamp = float(payload[0])

            self.gps.latitude = float(payload[1])
            self.gps.longitude = float(payload[3])

            self.gps.altitude = float(payload[8])

            self.gps.time = time_

            self.gps.convert_latitude()
            self.gps.convert_longitude()

            modified = True

        if("GLL" in type):

            self.gps.latitude = float(payload[0])
            self.gps.longitude = float(payload[2])

            self.gps.timestamp = float(payload[4])

            self.gps.time = time_

            self.gps.convert_latitude()
            self.gps.convert_longitude()

            modified = True

        if("RMC" in type):

            self.gps.timestamp = float(payload[0])

            self.gps.latitude = float(payload[2])
            self.gps.longitude = float(payload[4])

            self.gps.speed = float(payload[6])
            self.gps.course = float(payload[7])

            self.gps.time = time_

            self.gps.convert_latitude()
            self.gps.convert_longitude()

            modified = True

        return modified

    def __count_empty_elements(self, list):
        count = 0

        for e in list:
            if e == "":
                count += 1

        return count
