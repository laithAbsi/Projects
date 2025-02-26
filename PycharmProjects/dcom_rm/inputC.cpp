// This is a regular comment, not dated
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;

    // 15/07/2022: This function is updated to handle special cases
    int x = 5;  // A non-dated comment

    /*
     * 12/12/2021: Multi-line comment explaining the following block
     * This comment includes a date and should be removed.
     */
    if (x > 0) {
        std::cout << "x is positive" << std::endl;
    }

    /* Just a regular comment, not dated.
     * This comment will be retained.
     */

    // 01/01/2023: A single-line dated comment to be removed.

    return 0;
}
