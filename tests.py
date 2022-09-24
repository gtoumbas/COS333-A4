import os
import subprocess

CORRECT_REG="/u/cos333/Asgt1Solution/ref_reg.pyc"
CORRECT_REGDETAILS="/u/cos333/Asgt1Solution/ref_regdetails.pyc"

OUR_REG="reg.py"
OUR_REGDETAILS="regdetails.py"

def test_with_file(arg_file, correct_file, our_file):
    num_passed = 0
    num_failed = 0
    print("-----------------------------")
    print(f"Testing with {arg_file}")
    print(f"Correct File {correct_file}")
    print(f"Our File {our_file}")

    # Assert all files exist
    assert os.path.exists(arg_file)
    assert os.path.exists(correct_file)
    assert os.path.exists(our_file)

    # Read lines file into array of strings (including empty lines)
    args = []
    with open(arg_file) as f:
        for line in f:
            if line == '\n':
                args.append("")
            else:
                args.append(line.rstrip())

    for a in args:
        # Run correct file, capture output and errors
        try:
            if a == "":
                correct_output = subprocess.check_output(["python", correct_file], stderr=subprocess.STDOUT).decode()
            else:
                correct_output = subprocess.check_output(["python", correct_file, a], stderr=subprocess.STDOUT).decode()
        except subprocess.CalledProcessError as e:
            correct_output = e.output.decode()

        # Run our file, capture output and errors
        try:
            # Makes sure work with empty args
            if a == "":
                our_output = subprocess.check_output(["python", our_file], stderr=subprocess.STDOUT).decode()
            else:
                our_output = subprocess.check_output(["python", our_file, a], stderr=subprocess.STDOUT).decode()
        except subprocess.CalledProcessError as e:
            our_output = e.output.decode()

        # Compare outputs
        if correct_output != our_output:
            print(f"Failed with {a}")
            # Display max 5 lines where outputs differ
            count = 0
            print("--------------------------------")
            for c, o in zip(correct_output.splitlines(), our_output.splitlines()):
                if c != o:
                    print(f"Correct: \n{c}\n")
                    print(f"Ours: \n{o}\n\n\n")
                    count += 1
                    if count == 5:
                        break
            print("--------------------------------")
            num_failed += 1

        else:
            print(f"Passed with {a}")
            num_passed += 1
        
    print(f"\nPassed {num_passed} tests")
    print(f"Failed {num_failed} tests")
        

test_with_file('reg_test_args.txt', CORRECT_REG, OUR_REG)
test_with_file('regdetails_test_args.txt', CORRECT_REGDETAILS, OUR_REGDETAILS)
