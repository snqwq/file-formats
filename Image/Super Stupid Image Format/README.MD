# Super Stupid Image Format

custom image format for fun

## Specification

### File Structure

#### Header

| Name          | Offset | Data Type | Size | Description                |
| ------------- | ------ | --------- | ---- | -------------------------- |
| Magic         | 0x00   | char[4]   | 4    | Magic Number (SSIF)        |
| Major Version | 0x04   | uint8     | 1    | Major Version              |
| Minor Version | 0x05   | uint8     | 1    | Minor Version              |
| UTSOC         | 0x07   | uint32    | 4    | Unix Timestamp of Creation |
| Width         | 0x0B   | uint16    | 2    | Width of Image             |
| Height        | 0x0D   | uint16    | 2    | Height of Image            |
| CRC32         | 0x0F   | uint32    | 4    | CRC32 of Image Data        |
| EOH           | 0x1D   | char[3]   | 3    | End of Header (END)        |

#### Image Data
