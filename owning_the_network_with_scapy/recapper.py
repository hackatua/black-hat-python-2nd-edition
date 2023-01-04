from scapy.all import TCP, rdpcap
import collections
import os
import re
import sys
import zlib

OUTDIR = './trash'
PCAPS = '.'

Response = collections.namedtuple('Response', ['header', 'payload'])

def get_header(payload):
    try:
        header_raw = payload[:payload.index(b'\r\n\r\n') + 2]
    except ValueError:
        sys.stdout.write('-')
        sys.stdout.flush()
        return None
    
    header = dict(re.findall(
        r'(?P<name>.*?): (?P<value>.*?)\r\n',
        header_raw.decode()
    ))

    header = {k.lower(): v for k, v in header.items()}

    if 'content-type' not in header:
        return None
    return header

def extract_content(response, content_name='image'):
    content, content_type = None, None
    if content_name in response.header['content-type']:
        content_type = response.header['content-type'].split('/')[1]
        content = response.payload[response.payload.index(b'\r\n\r\n') + 4:]

        if 'content-encoding' in response.header:
            if response.header['content-encoding'] == 'gzip':
                content = zlib.decompress(
                    response.payload,
                    zlib.MAX_WBITS | 32
                )
            elif response.header['content-encoding'] == 'deflate':
                content = zlib.decompress(response.payload)
    
    return content, content_type

class Recapper:
    def __init__(self, pcap_file, out_dir):
        pcap = rdpcap(pcap_file)
        self.sessions = pcap.sessions()
        self.responses = list()
        self.out_dir = out_dir

    def get_responses(self):
        for session in self.sessions:
            payload = b''
            for packet in self.sessions[session]:
                try:
                    if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                        payload += bytes(packet[TCP].payload)
                except IndexError:
                    sys.stdout.write('x')
                    sys.stdout.flush()
            if payload:
                header = get_header(payload)
                if header is None:
                    continue
                self.responses.append(Response(header=header, payload=payload))
    
    def write(self, content_name):
        for i, response in enumerate(self.responses):
            content, content_type = extract_content(response, content_name)
            if content and content_type:
                file_name = os.path.join(self.out_dir, f'ex_{i}.{content_type}')
                print(f'Writing {file_name}')
                with open(file_name, 'wb') as file:
                    file.write(content)

def main():
    (pcap_file, out_dir) = (sys.argv[1], sys.argv[2])
    recapper = Recapper(pcap_file, out_dir)
    recapper.get_responses()
    print()
    print(pcap_file, out_dir)
    recapper.write('image')

if __name__ == '__main__':
    main()