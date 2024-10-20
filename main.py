import math
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--type", action="store", default=None, type=str,
                    help="What type of loan is this, annuity or differentiated? Enter 'annuity' or 'diff'")

parser.add_argument("--principal", action="store", default=None, type=float,
                    help="Enter the loan principal")
parser.add_argument("--periods", action="store", default=None, type=float,
                    help="Enter the number of months needed to repay the loan. It's calculated based on "
                         "the interest, annuity payment, and principal.")
parser.add_argument("--interest", action="store", default=None, type=float,
                    help="Enter the interest rate - is specified without a percent sign. Note that it can accept a "
                         "floating-point value. The loan calculator can't calculate the interest, "
                         "so it must always be provided.")
parser.add_argument("--payment", action="store", default=None, type=float,
                    help="Enter the payment amount. ")

args = parser.parse_args()


def annuity_periods():  # Calculating the Number of Monthly Payments: --periods
    global y, overpayment
    i = args.interest / (12 * 100)
    n = math.ceil(math.log(args.payment / (args.payment - (i * args.principal)), 1 + i))
    y = divmod(n, 12)
    total_payment = args.payment * n
    overpayment = math.ceil(total_payment - args.principal)
    return y, overpayment


def annuity_payment():  # Calculating the monthly payment (annuity) --payment
    global d, overpayment
    i = args.interest / (12 * 100)
    d = math.ceil((((1 + i) ** args.periods) * i * args.principal) / (((1 + i) ** args.periods) - 1))
    total_payment = d * args.periods
    overpayment = math.ceil(total_payment - args.principal)
    return d, overpayment


def annuity_principal():  # Calculating Loan Principal --principal
    global p, overpayment
    i = args.interest / (12 * 100)
    p = round((args.payment * (((1 + i) ** args.periods) - 1)) / (((1 + i) ** args.periods) * i))
    total_sum = args.payment * args.periods
    overpayment = math.ceil(total_sum - p)
    return p, overpayment


def differentiated_payments(): # Example Parameters: --type=diff --principal=1000000 --periods=10 --interest=10
    i = args.interest / (12 * 100)
    payments = []
    for n in range(1, int(args.periods) + 1):
        d = math.ceil((args.principal / args.periods) +
                      (i * (args.principal - ((args.principal * (n - 1)) / args.periods))))
        print(f"Month {n}: payment is {d}")
        payments.append(d)
    print('')
    total_payment = sum(payments)
    overpayment = math.ceil(total_payment - args.principal)
    print(f"Overpayment: {overpayment}")
    return overpayment, total_payment


# Negative Parameter Input Check
if args.principal != None and args.principal <= 0:
    print("Incorrect Parameters")
elif args.interest != None and args.interest <= 0:
    print("Incorrect Parameters")
elif args.payment != None and args.payment <= 0:
    print("Incorrect Parameters")
elif args.periods != None and args.periods <= 0:
    print("Incorrect Parameters")

else:
    # If the User Chooses --type as "annuity":
    if args.type == "annuity":
        # Example Parameters: --type=annuity --principal=1000000 --payment=15000 --interest=10
        if args.periods == None and None not in (args.principal, args.interest, args.payment):
            annuity_periods()
            if y[1] != 0:
                print(f"It will take {int(y[0])} years and {math.ceil(y[1])} months to repay the loan!", end="\n\n")
                print(f"Overpayment: {overpayment}")
            elif y[1] == 0:
                print(f"It will take {int(y[0])} years to repay the loan!", end="\n\n")
                print(f"Overpayment: {overpayment}")

        # Example Parameters: --type=annuity --principal=1000000 --periods=60 --interest=10
        elif args.payment == None and None not in (args.principal, args.interest, args.periods):
            annuity_payment()
            print(f'Your monthly payment = {d}!', end="\n\n")
            print(f"Overpayment: {overpayment}")
        # Example Parameters: --type=annuity --payment=8721.8 --periods=120 --interest=5.6
        elif args.principal == None and None not in (args.interest, args.payment, args.periods):
            annuity_principal()
            print(f'Your loan principal = {p}!', end="\n\n")
            print(f"Overpayment: {overpayment}")
        else:
            print("Incorrect parameters: Passed args.test check and went into else block since if/elif checks failed")


    # If the user chooses --type as "diff":
    # Example Parameters: --type=diff --principal=1000000 --periods=10 --interest=10
    elif args.type == "diff":
        if args.payment == None and None not in (args.principal, args.interest, args.periods):
            differentiated_payments()
        else:
            print("Incorrect parameters")
            #print("You went into the \"diff\" type category, then went into the else statement - issue with args.payment")


    else:
        print("Incorrect parameters")
