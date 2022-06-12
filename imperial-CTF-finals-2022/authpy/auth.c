#include <stdio.h>
#include <stdbool.h>

static bool authenticated = false;

void authenticate(char *user) {
    if (user == "1337_H4X0R")
        authenticated = true;
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    char username[64];

    printf("Enter your username: ");
    scanf("%63s", username);

    printf("Authenticating user: ");
    printf(username);
    printf("...\n");

    authenticate(username);

    if (authenticated) {
        printf("Access granted, enjoy your shell!\n");
        system("/bin/sh");
    } else {
        printf("Access Denied!\n");
    }

    return 0;
}