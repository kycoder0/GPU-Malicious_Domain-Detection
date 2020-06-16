import pycuda
import pycuda.driver as drv
drv.init()

class Devices:

    def __init__(self):
        self.num_devices = drv.Device.count()

    def get_info(self, device_number):
        info = ""
        if 0 <= device_number < self.num_devices:
            gpu_device = drv.Device(device_number)
            info += 'Device {}: {}'.format(device_number, gpu_device.name()) + '\n'

            compute_capability = float( '%d.%d' % gpu_device.compute_capability() )
            info += '\t Compute Capability: {}'.format(compute_capability) + '\n'
            info += '\t Total Memory: {} megabytes'.format(gpu_device.total_memory()//(1024**2)) + '\n'

            device_attributes_tuples = gpu_device.get_attributes().items()
            device_attributes = {}
            for k, v in device_attributes_tuples:
                device_attributes[str(k)] = v
            num_mp = device_attributes['MULTIPROCESSOR_COUNT']
            cuda_cores_per_mp = { 5.0 : 128, 5.1 : 128, 5.2 : 128, 6.0 : 64, 6.1 : 128, 6.2 : 128, 7.5 : 128}[compute_capability]
            info += '\t ({}) Multiprocessors, ({}) CUDA Cores / Multiprocessor: {} CUDA Cores'.format(num_mp, cuda_cores_per_mp, num_mp*cuda_cores_per_mp) + '\n'
            device_attributes.pop('MULTIPROCESSOR_COUNT')
            for k in device_attributes.keys():
                info += '\t {}: {}'.format(k, device_attributes[k])
                info += '\n'

            return info

device = Devices()

print(device.get_info(0))