#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define BUFFER_SIZE 256 // 缓冲区大小

// 反转数字部分的函数
void reverse_data(const char *input, char *output) {
    size_t len = strlen(input);
    int start = 0, end = len - 1;

    // 查找数字部分的起始和结束位置
    while (start < len && !isdigit(input[start]) && input[start] != '.') start++;
    while (end >= 0 && !isdigit(input[end]) && input[end] != '.') end--;

    // 反转数字部分
    int j = 0;
    for (int i = end; i >= start; i--) {
        output[j++] = input[i];
    }
    output[j] = '\0'; // 添加字符串结束符
}

// 发送数据到串口
void send_data(HANDLE hSerial, const char *data) {
    DWORD bytesWritten;
    if (!WriteFile(hSerial, data, strlen(data), &bytesWritten, NULL)) {
        printf("Error writing to serial port!\n");
    } else {
        printf("Sent: %s\n", data);
    }
}

int main() {
    HANDLE hSerial;
    DCB dcbSerialParams = {0};
    COMMTIMEOUTS timeouts = {0};

    // 打开串口 COM3
    hSerial = CreateFile(
        "COM2",            // 串口号
        GENERIC_READ | GENERIC_WRITE, // 读写模式
        0,                 // 独占访问
        NULL,              // 默认安全属性
        OPEN_EXISTING,     // 打开已存在的设备
        0,                 // 非重叠模式
        NULL);             // 无模板文件

    if (hSerial == INVALID_HANDLE_VALUE) {
        printf("Error opening serial port!\n");
        return 1;
    }

    // 配置串口参数
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
    if (!GetCommState(hSerial, &dcbSerialParams)) {
        printf("Error getting serial port state!\n");
        CloseHandle(hSerial);
        return 1;
    }

    dcbSerialParams.BaudRate = CBR_9600; // 波特率 9600
    dcbSerialParams.ByteSize = 8;        // 数据位 8
    dcbSerialParams.StopBits = ONESTOPBIT; // 停止位 1
    dcbSerialParams.Parity = NOPARITY;     // 无校验位

    if (!SetCommState(hSerial, &dcbSerialParams)) {
        printf("Error setting serial port state!\n");
        CloseHandle(hSerial);
        return 1;
    }

    // 配置超时
    timeouts.ReadIntervalTimeout = 50; // 间隔超时
    timeouts.ReadTotalTimeoutConstant = 50;
    timeouts.ReadTotalTimeoutMultiplier = 10;

    if (!SetCommTimeouts(hSerial, &timeouts)) {
        printf("Error setting timeouts!\n");
        CloseHandle(hSerial);
        return 1;
    }

    // 读取数据
    char buffer[BUFFER_SIZE];
    char reversed_buffer[BUFFER_SIZE];
    DWORD bytesRead;
    printf("Reading data from serial port...\n");

    while (1) {
        if (ReadFile(hSerial, buffer, BUFFER_SIZE - 1, &bytesRead, NULL)) {
            if (bytesRead > 0) {
                buffer[bytesRead] = '\0'; // 添加字符串结束符
                reverse_data(buffer, reversed_buffer); // 反转数据
                printf("Received (reversed): %s\n", reversed_buffer); // 输出到控制台

                // 检测是否收到字符 'R'
                if (strchr(buffer, 'R') != NULL) {
                    // 构造数据格式 0199.97
                    char send_buffer[16];
                    int integer_part = 199;    // 假定整数部分
                    int decimal_part = 97;    // 假定小数部分
                    sprintf(send_buffer, "%04d.%02d", integer_part, decimal_part);

                    // 发送到串口
                    send_data(hSerial, send_buffer);
                }
            }
        } else {
            printf("Error reading from serial port!\n");
            break;
        }
    }

    // 关闭串口
    CloseHandle(hSerial);
    return 0;
}
