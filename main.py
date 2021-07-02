import requests
import hashlib


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError(f'Error while fetching the data. Error:{res.status_code}')
    return res


def leak_counts(hashes, check_hash):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == check_hash:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return leak_counts(response, tail)


def main(pswd):
    counted = pwned_api_check(pswd)
    if counted:
        print(f'Your Password ({pswd}) was found {counted} times hacked!!')
        print('Change your password immediately!')
    else:
        print(f'{pswd} was not found.')
        print('Carry on!')


get_password = input("Enter Your Password: ")
main(get_password)
