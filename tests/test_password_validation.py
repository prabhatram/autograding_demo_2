import subprocess
import pytest

def run_student_script(inputs):
    try:
        # Run the student's script using subprocess
        process = subprocess.Popen(
            ['python3', 'string_and_loop.py'],  # Adjust the path if necessary
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Communicate with the process (send inputs and capture output)
        stdout, stderr = process.communicate(input="\n".join(inputs) + "\n", timeout=10)
        
        if stderr:
            print("Error occurred while running the student's script:")
            print(stderr)
        
        return stdout.strip(), stderr.strip()

    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        print("The student's script took too long to run and was terminated.")
        return stdout.strip(), stderr.strip()

def test_invalid_username():
    stdout, _ = run_student_script(["user!name", "username1", "Password1!"])
    assert "Invalid username. Only alphabets and numbers are allowed." in stdout
    assert "Both username and password are valid!" in stdout

def test_valid_username_invalid_password_no_special_char():
    stdout, _ = run_student_script(["username1", "Password123", "Password1!"])
    assert "Invalid password. Password must contain letters, numbers, at least one special character, and at least one uppercase letter." in stdout
    assert "Both username and password are valid!" in stdout

def test_valid_username_invalid_password_no_uppercase():
    stdout, _ = run_student_script(["username1", "password1!", "Password1!"])
    assert "Invalid password. Password must contain letters, numbers, at least one special character, and at least one uppercase letter." in stdout
    assert "Both username and password are valid!" in stdout

def test_valid_username_invalid_password_no_digit():
    stdout, _ = run_student_script(["username1", "Password!", "Password1!"])
    assert "Invalid password. Password must contain letters, numbers, at least one special character, and at least one uppercase letter." in stdout
    assert "Both username and password are valid!" in stdout

def test_valid_username_valid_password():
    stdout, _ = run_student_script(["username1", "Password1!"])
    assert "Both username and password are valid!" in stdout
