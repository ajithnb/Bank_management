
import mysql.connector


class Bank_management:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ajiThh**#110",
            database="bank_management"
        )
        print("Connected Successfully....!")

    def post(self, **kwargs):
        try:
            if float(kwargs["balance"]) < 0:
                print("Opening balance cannot be negative!")
                return

            self.cursor = self.connection.cursor()

            query = """
                INSERT INTO accounts
                (customer_name, account_type, phone, balance)
                VALUES (%s, %s, %s, %s)
            """

            values = (
                kwargs["customer_name"],
                kwargs["account_type"],
                kwargs["phone"],
                kwargs["balance"],
            )

            self.cursor.execute(query, values)
            self.connection.commit()
            print("Accounts created successfully")

        except Exception as e:
            self.connection.rollback()
            print(e)

    def get(self, minimum_balance=None):
        try:
            self.cursor = self.connection.cursor()

            if minimum_balance is not None:

                query = "select * from accounts WHERE balance >= %s ORDER BY balance DESC"
                values = (minimum_balance,)

                self.cursor.execute(query, values)

            else:

                query = "select * from accounts ORDER BY balance DESC"
                self.cursor.execute(query)

            records = self.cursor.fetchall()

            for data in records:
                print(data)

        except Exception as e:
            print(e)

    def get_object(self, id=None):
        try:
            self.cursor = self.connection.cursor()

            query = "select * from accounts WHERE account_id = %s"
            values = (id,)

            self.cursor.execute(query, values)
            record = self.cursor.fetchone()

            return record

        except Exception as e:
            print(e)
            return None

    def deposit(self, id=None, amount=None):
        try:
            if amount <= 0:
                print("Invalid amount!")
                return

            record = self.get_object(id=id)

            if record is not None:

                self.cursor = self.connection.cursor()

                query = """
                    update accounts
                    set balance = balance + %s
                    WHERE account_id = %s
                """

                values = (amount, id)

                self.cursor.execute(query, values)
                self.connection.commit()

                print("Amount deposited successfully...!")

            else:
                print("Account not found...!")

        except Exception as e:
            self.connection.rollback()
            print(e)

    def withdraw(self, id=None, amount=None):
        try:
            if amount <= 0:
                print("Invalid amount!")
                return

            self.cursor = self.connection.cursor()

            query = """
                update accounts
                set balance = balance - %s
                WHERE account_id = %s AND balance >= %s
            """

            values = (amount, id, amount)

            self.cursor.execute(query, values)
            self.connection.commit()

            if self.cursor.rowcount > 0:
                print("Amount withdrawn successfully...!")

            else:
                record = self.get_object(id=id)

                if record is None:
                    print("Account not found...!")
                else:
                    print("Insufficient balance...!")

        except Exception as e:
            self.connection.rollback()
            print(e)

    def delete(self, id=None):
        try:
            record = self.get_object(id=id)

            if record is not None:

                self.cursor = self.connection.cursor()

                query = "delete from accounts WHERE account_id = %s"
                values = (id,)

                self.cursor.execute(query, values)
                self.connection.commit()

                print("Accounts deleted successfully...!")

            else:
                print("Accounts not found...!")

        except Exception as e:
            self.connection.rollback()
            print(e)


bank = Bank_management()

while True:

    print("-- bank_management __")
    print("1. Create acc")
    print("2. View all acc")
    print("3. Deposit amount")
    print("4. Withdraw amount")
    print("5. Delete account")
    print("6. Exit")

    try:
        choice = int(input("Enter your choice: "))

        if choice == 1:

            customer_name = input("Enter customer name: ")
            account_type = input("Enter account type: ")
            phone = input("Enter phone number: ")
            balance = float(input("Enter opening balance: "))

            bank.post(
                customer_name=customer_name,
                account_type=account_type,
                phone=phone,
                balance=balance
            )

        elif choice == 2:

            minimum_balance = input(
                "Enter minimum balance : "
            )

            if minimum_balance == "":
                bank.get()
            else:
                bank.get(minimum_balance=float(minimum_balance))

        elif choice == 3:

            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter deposit amount: "))

            bank.deposit(account_id, amount)

        elif choice == 4:

            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter withdrawal amount: "))

            bank.withdraw(account_id, amount)

        elif choice == 5:

            account_id = int(input("Enter account ID to delete: "))

            confirmation = input(
                "Are you sure you want to delete? (ys/no): "
            )

            if confirmation.lower() == "yes":
                bank.delete(account_id)
            else:
                print("Deltion cancelled")

        elif choice == 6:

            print("Thanku")

            bank.connection.close()
            break

        else:
            print("Invalid")

    except ValueError:
        print("Please enter a valid input")

    except Exception as e:
        print(e)
