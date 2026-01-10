# Minimal stub for SQLAlchemy symbols used in orm.py when SQLAlchemy is not installed.
# This file provides dummy classes/functions so that imports succeed
# without pulling in the actual SQLAlchemy package.

class Column:
    def __init__(self, *args, **kwargs):
        pass

class String:
    def __init__(self, *args, **kwargs):
        pass

class DateTime:
    def __init__(self, *args, **kwargs):
        pass

class Float:
    def __init__(self, *args, **kwargs):
        pass

class ForeignKey:
    def __init__(self, *args, **kwargs):
        pass

def relationship(*args, **kwargs):
    return None

# Base class placeholder for declarative models
class Base:
    pass

# Dummy ORM model classes matching the real ones used elsewhere.
class Goal(Base):
    pass

class Family(Base):
    pass

class FamilyMember(Base):
    pass

class Document(Base):
    pass

class Transaction(Base):
    pass

class MonthlySummary(Base):
    pass
