import io
from v4l2py import Device, IO, Frame


class Kamera:
    """
    Simplified interface to v4l2py in order to get higher quality images for machine vision applications
    - Alexander Goldhill
    """
    def __init__(self, devId: int = 0) -> None:
        """
        Args:
            devId (int): the device id to open as imaging device, default /dev/video0
        """
        self.kamera = Device.from_id(devId)
        self.kamera.open()

    def show_info(self) -> None:
        print(self.kamera.info.card)

    def show_capabilities(self) -> None:
        print(self.kamera.info.capabilities)

    def show_formats(self) -> None:
        print(self.kamera.info.formats)

    def show_all_controls(self, ctrls: list = None) -> None:
        for ctrl in self.kamera.controls.values():
            print(ctrl)

    def get_option_value_type(self, option: str) -> type:
        return type(self.kamera.controls[option])

    def set_control(self, option: str, value, verbose: bool = False) -> None:
        ctrl = self.kamera.controls[option]
        oldval, ctrl.value = ctrl.value, value
        if (verbose): print(f'{option}: {oldval} -> {value}')

    def set_controls(self, ctrlValPairs: dict, verbose: bool = False) -> None:
        for ctrl, value in ctrlValPairs.items():
            self.set_control(ctrl, value, verbose)

    def show_format(self, fmt):
        pass

    def get_format(self, fmt: int):
        return self.kamera.get_format(fmt)

    def set_format(self, format):
        # 
        pass

    def get_control(self, option: str):
        return self.kamera.controls[option]
    
    def set_control_default(self, ctrl):
        pass # TODO
    
    def capture(self, filename: str) -> int:
        """
        Args:
            file (str): Path to save images to
        Returns:
            int: Amount of frames captured
        """
        cam = self.kamera

        with open(filename, 'wb') as file:
            for i, frame in enumerate(cam):
                file.write(bytes(frame.data))
                print(f"Wrote to file {filename}")
                break
        
        return 1


def main(args = None):
    import argparse
    #if (len(args) == 0): help(Kamera)
    kamera = Kamera(0)
    kamera.show_formats()
    #kamera.get_format()
    init_settings = {
        'white_balance_automatic': 0,
        'brightness': 128,
    }
    kamera.set_controls(init_settings, True)
    kamera.show_all_controls()
    #kamera.capture('test.jpg')

if __name__ == '__main__':
    main()