# Super Stupid Image Format

> [!NOTE]
> This image format is in no way practical, efficent, or useful.
> It was created for fun and educational purposes. (me trying to learn how to create a file format)

## Specification

- RGB565 (16 bit) Color Format
- .ssif file extension

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
