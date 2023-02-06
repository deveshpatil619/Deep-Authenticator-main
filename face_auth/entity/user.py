import uuid


class User:
    ## The __init__ method is the constructor of the class, which is used to initialize the class attributes.
    #  The class attributes are Name, username, email_id, ph_no, password1, password2 and uuid_. 
    # When a new object of the class is created, these attributes are initialized with the values passed to the constructor.
    def __init__(self,Name: str,username: str,email_id: str,ph_no: str,password1: str,password2: str,
    uuid_: str = None,):

        self.Name = Name
        self.username = username
        self.email_id = email_id
        self.ph_no = ph_no
        self.password1 = password1
        self.password2 = password2
        self.uuid_ = uuid_
        ##If uuid_ is not provided, it generates a new uuid using uuid.uuid4() function twice,
        # and concatenates the first 4 characters of the second generated uuid to the first generated
        #  uuid to form a new uuid.
        if not self.uuid_:
            self.uuid_ = str(uuid.uuid4()) + str(uuid.uuid4())[0:4]

    def to_dict(self) -> dict:  ## The to_dict method returns the class attributes in a dictionary form.
        return self.__dict__

    def __str__(self) -> str:  
        ## The __str__ method returns the string representation of the class attributes that are 
        ## in dictionary form, which is obtained by calling the to_dict method.
        return str(self.to_dict())
