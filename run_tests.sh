# Reads arguments from reg_test_args.txt and regdetails_test_args.txt
# Compares both output and errors outputed 

CORRECT_REG="/u/cos333/Asgt1Solution/ref_reg.pyc"
CORRECT_REGDETAILS="/u/cos333/Asgt1Solution/ref_regdetails.pyc"

OUR_REG="reg.py"
OUR_REGDETAILS="regdetails.py"


test_with_file (){
    arg_file=$1
    correct_file=$2
    our_file=$3

    # Print these 3
    printf "\nTesting with $arg_file\n"
    printf "Correct file: $correct_file\n"
    printf "Our file: $our_file\n\n"

    while read line
    do

        python $correct_file $line > correct_output.txt 2> correct_error.txt
        python $our_file $line > our_output.txt 2> our_error.txt

        # Check any errors occured in correct program
        if [ -s correct_error.txt ]
        then
            if ! diff correct_error.txt our_error.txt > /dev/null
            then
                printf 'Errors differ with input: %s \n' "$line"
                printf 'Correct Error: %s \n' "$(cat correct_error.txt)"
                printf '\nOur Error: %s \n' "$(cat our_error.txt)\n"
                continue
            else 
                printf "Output same error on args: %s \n" "$line"
                continue
            fi
        fi

        if diff correct_output.txt our_output.txt > /dev/null # Compare outputs 
        then
            printf 'PASS %s\n' "${line}"
        else
            printf 'FAIL %s\n' "${line}"
            printf "Diff:\n"
            diff correct_output.txt our_output.txt
            printf "\n"
        fi

        # Clear output files
        > correct_output.txt
        > our_output.txt
        > correct_error.txt
        > our_error.txt

    done < $arg_file
}

test_with_file "reg_test_args.txt" $CORRECT_REG $OUR_REG
test_with_file "regdetails_test_args.txt" $CORRECT_REGDETAILS $OUR_REGDETAILS

# Clean up
trap "rm -f correct_output.txt our_output.txt correct_error.txt our_error.txt" EXIT