// tcp_epoll_server.cpp
#include <arpa/inet.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <unistd.h>

#include <cerrno>
#include <cstring>
#include <iostream>
#include <vector>

constexpr int MAX_EVENTS = 4096;
constexpr int BUFFER_SIZE = 4096;

static int make_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags == -1) return -1;
    return fcntl(fd, F_SETFL, flags | O_NONBLOCK);
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <port>\n";
        return 1;
    }

    int port = std::stoi(argv[1]);

    int listen_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_fd == -1) {
        perror("socket");
        return 1;
    }

    int opt = 1;
    setsockopt(listen_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(port);

    if (bind(listen_fd, (sockaddr*)&addr, sizeof(addr)) == -1) {
        perror("bind");
        return 1;
    }

    if (make_nonblocking(listen_fd) == -1) {
        perror("nonblocking");
        return 1;
    }

    if (listen(listen_fd, SOMAXCONN) == -1) {
        perror("listen");
        return 1;
    }

    int epoll_fd = epoll_create1(0);
    if (epoll_fd == -1) {
        perror("epoll_create1");
        return 1;
    }

    epoll_event ev{};
    ev.events = EPOLLIN | EPOLLET;
    ev.data.fd = listen_fd;

    if (epoll_ctl(epoll_fd, EPOLL_CTL_ADD, listen_fd, &ev) == -1) {
        perror("epoll_ctl");
        return 1;
    }

    std::vector<epoll_event> events(MAX_EVENTS);
    char buffer[BUFFER_SIZE];

    std::cout << "Server listening on port " << port << "\n";

    while (true) {
        int n = epoll_wait(epoll_fd, events.data(), MAX_EVENTS, -1);
        if (n == -1) {
            if (errno == EINTR) continue;
            perror("epoll_wait");
            break;
        }

        for (int i = 0; i < n; ++i) {
            int fd = events[i].data.fd;

            if (fd == listen_fd) {
                // Accept all pending connections
                while (true) {
                    sockaddr_in client{};
                    socklen_t len = sizeof(client);
                    int client_fd = accept(listen_fd, (sockaddr*)&client, &len);
                    if (client_fd == -1) {
                        if (errno == EAGAIN || errno == EWOULDBLOCK)
                            break;
                        perror("accept");
                        break;
                    }

                    make_nonblocking(client_fd);

                    epoll_event client_ev{};
                    client_ev.events = EPOLLIN | EPOLLET;
                    client_ev.data.fd = client_fd;
                    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, client_fd, &client_ev);
                }
            } else {
                // Handle client I/O
                while (true) {
                    ssize_t count = recv(fd, buffer, sizeof(buffer), 0);
                    if (count == -1) {
                        if (errno == EAGAIN || errno == EWOULDBLOCK)
                            break;
                        close(fd);
                        break;
                    } else if (count == 0) {
                        close(fd);
                        break;
                    } else {
                        // Echo back
                        ssize_t sent = 0;
                        while (sent < count) {
                            ssize_t n = send(fd, buffer + sent, count - sent, 0);
                            if (n == -1) {
                                if (errno == EAGAIN || errno == EWOULDBLOCK)
                                    break;
                                close(fd);
                                goto next_event;
                            }
                            sent += n;
                        }
                    }
                }
            }
        next_event:;
        }
    }

    close(listen_fd);
    close(epoll_fd);
    return 0;
}
