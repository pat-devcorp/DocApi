class MockBrokerClient:
    def dsn(self):
        return "mock-broker"

    def publish(self, message) -> None:
        return None
