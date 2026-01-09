import platform
import numpy as np


OS = platform.system().lower()




class SystemVolumeControl:
    def __init__(self):
        self.volume = None
        self.min_db = 0
        self.max_db = 0
        self.target_max_db_override = None # Ajuste personalizado

        self.os_type = OS

        if self.os_type == 'windows':
            try:
                # Importamos aqui dentro para o Linux não tentar ler isso
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                from comtypes import CLSCTX_ALL
                import ctypes
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                self.volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
                self.min_db, self.max_db, _ = self.volume.GetVolumeRange()
            except Exception as e:
                print(f"Erro ao iniciar volume no Windows: {e}")

        elif self.os_type == 'linux':
            try:
                import alsaaudio
                # No Linux usamos o Mixer 'Master'
                self.mixer = alsaaudio.Mixer('Master')
                self.volume = True # Apenas para o seu main.py saber que está ativo
                print("Controle de volume Linux (ALSA) iniciado.")
            except Exception as e:
                print(f"Erro ao iniciar volume no Linux: {e}")
        else:
            print('SISTEMA OPERACIONAL NÃO SUPORTADO')


    def set_max_db_override(self, max_db_value: float):
        """Permite definir um valor máximo de dB personalizado."""
        self.target_max_db_override = max_db_value
        
    def set_volume_percentage(self, length: float, HAND_DIST_MIN: int, HAND_DIST_MAX: int):
        # Cálculo básico de porcentagem (0 a 100)
        vol_percent = np.interp(length, [HAND_DIST_MIN, HAND_DIST_MAX], [0, 100])
        vol_percent = np.clip(vol_percent, 0, 100)

        if self.os_type == 'windows' and self.volume:
            import numpy as np
            vol_db = np.interp(length, [HAND_DIST_MIN, HAND_DIST_MAX], [self.min_db, self.max_db])
            self.volume.SetMasterVolumeLevel(vol_db, None)

        elif self.os_type == 'linux' and self.mixer:
            # O ALSA usa valores de 0 a 100 diretamente
            self.mixer.setvolume(int(vol_percent))

        return vol_percent