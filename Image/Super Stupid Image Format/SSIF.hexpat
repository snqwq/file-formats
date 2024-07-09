#pragma author bavib
#pragma description Super Stupid Image Format

char magic [0x04] @ 0x00;
u8 major_version @ 0x04;
u8 minor_version @ 0x05;
bool is_randal_in_my_computer @ 0x06;
u32 unix_timestamp_of_creation @ 0x07;
u16 width @ 0x0B;
u16 height @ 0x0D;
u32 CRC32_of_image_data @ 0x0F;
char end_of_header[0x03] @ 0x1D;