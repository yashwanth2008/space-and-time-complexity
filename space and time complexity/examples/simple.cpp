#include <iostream>
#include <string>
using namespace std;

class transaction {
private:
    int sender_id;
    int balance;
    int receiver_id;
    float amount;

public:
    void t1(int sender, int currentBalance, int receiver, float transactionAmount) {
        sender_id = sender;
        balance = currentBalance;
        receiver_id = receiver;
        amount = transactionAmount;

        cout << sender_id << " sends the amount " << amount
             << " to " << receiver_id << endl;
        cout << "The remaining amount is "
             << (balance - amount) << endl;
    }
};

int main() {
    transaction t;

    t.t1(5432, 5000, 8675, 500);
    t.t1(5432, 5430, 8675, 500);
    return 0;
}