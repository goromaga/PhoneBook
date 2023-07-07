import os
import sys
import typing


class PhoneBookEntry:
    """
    A phone book entry.

    Attributes:
        name: The name of the person.
        surname: The surname of the person.
        separator: The separator between the name and surname.
        phone_number: The phone number of the person.
    """

    def __init__(self, name: str = '', surname: str = '', separator: str = '', phone_number: str = ''):
        """
        Initialize a phone book entry.

        Args:
            name: The name of the person.
            surname: The surname of the person.
            separator: The separator between the name and surname.
            phone_number: The phone number of the person.
        """
        self._name = name
        self._surname = surname
        self._separator = separator
        self._phoneNumber = phone_number

    @property
    def name(self) -> str:
        """Get the name of the person."""
        return self._name

    @name.setter
    def name(self, name: str):
        """Set the name of the person."""
        if not name:
            raise ValueError("Name cannot be empty")
        self._name = name

    @property
    def surname(self) -> str:
        """Get the surname of the person."""
        return self._surname

    @surname.setter
    def surname(self, surname: str):
        """Set the surname of the person."""
        if not surname:
            raise ValueError("Surname cannot be empty")
        self._surname = surname

    @property
    def separator(self) -> str:
        """Get the separator between the name and surname."""
        return self._separator

    @separator.setter
    def separator(self, separator: str):
        """Set the separator between the name and surname."""
        if separator not in ("-", ":"):
            raise ValueError("Separator must be '-' or ':'")
        self._separator = separator

    @property
    def phone_number(self) -> str:
        """Get the phone number of the person."""
        return self._phoneNumber

    @phone_number.setter
    def phone_number(self, phone_number: str):
        """Set the phone number of the person."""
        if not phone_number.isdigit():
            raise ValueError("Phone number must be numeric")
        if len(phone_number) != 9:
            raise ValueError("Phone number must be 9 digits long")
        self._phoneNumber = phone_number

    def __repr__(self) -> str:
        """Get a string representation of the phone book entry."""
        return f"{self.name} {self.surname} {self.separator} {self.phone_number}"


def read_phone_book(file_path: str) -> typing.List[PhoneBookEntry] or None:
    """
    Read the phone book entries from a file.

    Args:
        file_path: The path to the file.

    Returns:
        A list of phone book entries.
    """
    phone_book_entries = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                values = line.strip().split()
                if len(values) == 4:
                    name, surname, separator, phone_number = values
                    phone_book_entry = PhoneBookEntry(name, surname, separator, phone_number)
                    phone_book_entries.append(phone_book_entry)
                elif len(values) == 3:
                    name, separator, phone_number = values
                    phone_book_entry = PhoneBookEntry(name=name, separator=separator, phone_number=phone_number)
                    phone_book_entries.append(phone_book_entry)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)
    return phone_book_entries


def sort_phone_book(phone_book_entries: typing.List[PhoneBookEntry], criteria: str = '', ordering: str = '') -> \
        typing.List[PhoneBookEntry]:
    """
    Sort the phone book entries by a given criteria.

    Args:
        phone_book_entries: The list of phone book entries.
        criteria: The criteria to sort by.
        ordering: The ordering, ascending or descending.

    Returns:
        The sorted list of phone book entries.
    """
    if criteria in {'name', 'surname', 'phone_number'}:
        key = lambda phone_book_entry: getattr(phone_book_entry, criteria, None)
    else:
        print("War: Wrong criteria, please choose one of this [Name, Surname, Phone_Number] ")
        sys.exit(1)
    reverse = ordering == "descending"
    return sorted(phone_book_entries, key=key, reverse=reverse)


def validate_phone_book_entry(phone_book_entry: PhoneBookEntry) -> list:
    """
    Validate a phone book entry.

    Args:
        phone_book_entry: The phone book entry to validate.

    Returns:
        An error message if the phone book entry is invalid, or None if the phone book entry is valid.
    """
    validate_mess: typing.List[str] = []
    if not phone_book_entry.name:
        validate_mess.append("Name cannot be empty")
    if not phone_book_entry.phone_number.isdigit():
        validate_mess.append("phone number must be numeric")
    if len(phone_book_entry.phone_number) != 9:
        validate_mess.append("phone number must be 9 digits")
    if phone_book_entry.separator not in (':', '-'):
        validate_mess.append("the separator should be `:` or `-`")
    return validate_mess


def main():
    file_path = input("File Path - ").strip()
    try:
        abs_path = os.path.abspath(os.path.join(os.getcwd(), file_path))
    except Exception as e:
        print(f"An error occurred while converting the file path to absolute path: {e}")
        sys.exit(1)
    phone_book_entries = read_phone_book(abs_path)
    criteria = input("Please choose criteria: “Name”, “Surname” or “Phone_Number”: ").strip().lower()
    ordering = input("Please choose ordering (Ascending or Descending): ").strip().lower()
    phone_book_entries = sort_phone_book(phone_book_entries, criteria, ordering)
    validation_messages = []
    print("\nFile Structure:")
    for phone_book_entry in phone_book_entries:
        print(phone_book_entry)
        validation_message = validate_phone_book_entry(phone_book_entry)
        if validation_message:
            validation_messages.append(validation_message)
    if validation_messages:
        print("\nValidations:")
        for i, validation_message in enumerate(validation_messages):
            print(f"line{i+1}: {', '.join(validation_message)}.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
