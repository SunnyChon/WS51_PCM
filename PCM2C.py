from datetime import datetime
import sys
import os

def file_to_c_array(file_path, output_path=None):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return
    with open(file_path, 'rb') as f:
        data = f.read()

    file_size = len(data)
    hex_lines = []
    for i in range(0, file_size, 12):
        chunk = data[i:i+12]
        hex_chunk = ", ".join([f"0x{b:02x}" for b in chunk])
        hex_lines.append("    " + hex_chunk)
    c_array_content = ",\n".join(hex_lines)
    output_text_a = f"""
/* Code by SunnyAI , 2026 07 08
   PCM playback code for WS51F6240
   Maximum PCM data size : 16000B - 489B = 15511B (2.5851s / 6KHz)
*/	

/* Generated with WS51_PCM project , {datetime.now()} */

#include "WS51F6240.h"	

#define pcm_data_len {file_size}

const uint8_t code pcm_data[] = {{
{c_array_content}
}};
"""
    if playmode:
        output_text_b = """
void delayMicroseconds(unsigned long us)
{unsigned long i;unsigned long usp;usp = us/8;for (i = 0; i < usp; i++){;}}
	
void delay(unsigned int ms)
{delayMicroseconds(ms * 1000);}

void play_pcm(void)
{ 
	unsigned int i;
	for (i = 0;i < pcm_data_len;i++){
		delayMicroseconds(220); //Delay for 6kHz PCM sample , adjust if needed.
		PWM0DUTL=pcm_data[i];
	}
}

void main(void)
{ 
	delay(64);
	SCCON = 0x00;
    delay(1);
	PWM0PS = 0x00;
	P11F = 0x02;
	P00F = 0X03;
	PWM0CFG=0x00;
	PMEN = 0x3F;
	PMDAT = 0x00;
	PMSCON = 0xE4;
	PMSDL = 0x03;
	PMSDH = 0x00;
	PMSML = 0x03;
	PMSMH = 0x00;
	PWM0DUTL=0x00;
	PWM0DUTH=0x00;
	PWM0DIVL=0xFF;
	PWM0DIVH=0x00;
	PWMRUN=0xFF;
	PS0 = 0x01;
	EA = 0x01;
	P11 = 0x00;
	while(1){
    	play_pcm(); //Play PCM
        P11 = 0x01; //Playback done flag
    }
}
"""

    else:
        output_text_b = """
void delayMicroseconds(unsigned long us)
{unsigned long i;unsigned long usp;usp = us/8;for (i = 0; i < usp; i++){;}}
	
void delay(unsigned int ms)
{delayMicroseconds(ms * 1000);}

void play_pcm(void)
{ 
	unsigned int i;
	for (i = 0;i < pcm_data_len;i++){
		delayMicroseconds(220); //Delay for 6kHz PCM sample , adjust if needed.
		PWM0DUTL=pcm_data[i];
	}
}

void main(void)
{ 
	delay(64);
	SCCON = 0x00;
    delay(1);
	PWM0PS = 0x00;
	P11F = 0x02;
	P00F = 0X03;
	PWM0CFG=0x00;
	PMEN = 0x3F;
	PMDAT = 0x00;
	PMSCON = 0xE4;
	PMSDL = 0x03;
	PMSDH = 0x00;
	PMSML = 0x03;
	PMSMH = 0x00;
	PWM0DUTL=0x00;
	PWM0DUTH=0x00;
	PWM0DIVL=0xFF;
	PWM0DIVH=0x00;
	PWMRUN=0xFF;
	PS0 = 0x01;
	EA = 0x01;
	P11 = 0x00;
	play_pcm(); //Play PCM
	P11 = 0x01; //Playback done flag
	while(1){}  //Do nothing
}
"""

    output_text = output_text_a + output_text_b
    if output_path:
        with open(output_path, 'w') as f:
            f.write(output_text)
        print(f"Successfully generated: {output_path}")
    else:
        print(output_text)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        os.system(f"ffmpeg -i \"{sys.argv[1]}\" -ac 1 -ar 6000 -t 2.58 -c pcm_u8 -f u8 pcm.bin")
        
        if len(sys.argv) > 2:
            playmode = int(sys.argv[2])
        else:
            playmode = 0
            
        if len(sys.argv) > 3:
            file_to_c_array("pcm.bin" , sys.argv[3])
        else:
            file_to_c_array("pcm.bin")
            
    else:
        print("Usage: python PCM2C.py <filename> [play mode , 0 = once/1 = loop , default = 0][output filepath]")
