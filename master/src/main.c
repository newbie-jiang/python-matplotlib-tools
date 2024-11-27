#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define BUFFER_SIZE 256 // 缓冲区大小

// 写入日志的函数
void log_to_file(const char *filename, const char *data) {
    FILE *file = fopen(filename, "a"); // 以追加模式打开文件
    if (file) {
        SYSTEMTIME st;
        GetLocalTime(&st); // 获取系统时间

        // 写入时间戳和数据
        fprintf(file, "[%04d-%02d-%02d %02d:%02d:%02d] %s\n",
                st.wYear, st.wMonth, st.wDay,
                st.wHour, st.wMinute, st.wSecond,
                data);

        fclose(file);
    } else {
        printf("Failed to open log file!\n");
    }
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

    // 提示用户输入时间间隔
    int interval_seconds;
    printf("Please enter the time interval (in seconds) for sending 'R': ");
    if (scanf("%d", &interval_seconds) != 1 || interval_seconds <= 0) {
        printf("Invalid input. Please enter a positive integer.\n");
        return 1;
    }

    // 打开串口 COM1
    hSerial = CreateFile(
        "COM1",            // 串口号
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
    DWORD bytesRead;
    printf("Reading data from serial port...\n");

    while (1) {
        // 每 interval_seconds 秒发送一次字符 'R'
        send_data(hSerial, "R");

        // 读取串口数据
        if (ReadFile(hSerial, buffer, BUFFER_SIZE - 1, &bytesRead, NULL)) {
            if (bytesRead > 0) {
                buffer[bytesRead] = '\0'; // 添加字符串结束符
                printf("Received: %s\n", buffer); // 输出到控制台

                // 写入日志文件
                log_to_file("serial_log.txt", buffer);
            }
        } else {
            printf("Error reading from serial port!\n");
            break;
        }

        // 每 interval_seconds 秒发送一次字符 'R'
        Sleep(interval_seconds * 800); // Sleep 以毫秒为单位，因此乘以 1000
    }

    // 关闭串口
    CloseHandle(hSerial);
    return 0;
}
