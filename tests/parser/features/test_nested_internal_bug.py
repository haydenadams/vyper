
def test_nested_internal_bug(get_contract, assert_tx_failed):
    passing_code = """
@private
def c() -> bool:
    return True

@private
def b(sender: address) -> address:
    assert self.c()
    return sender

@public
def a() -> bool:
    assert self.b(msg.sender) == msg.sender
    return True
    """

    failing_code = """
@private
def c(sender: address) -> address:
    return sender

@private
def b(sender: address) -> address:
    return self.c(sender)

@public
def a() -> bool:
    assert self.b(msg.sender) == msg.sender
    return True
    """

    passing_contract = get_contract(passing_code)
    failing_contract = get_contract(failing_code)
    assert passing_contract.a() == True
    assert_tx_failed(lambda: failing_contract.a())
