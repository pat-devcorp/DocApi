class TestTask:
    def get_invalid_task():
        return Task(
            taskId=0,
            channelType="A",
            requirement="asdasdasd",
            because="asdasdas",
            state="A",
            attrs=list(),
        )

    def get_valid_task(cls):
        identifier = cls.get_default_identifier()
        return Task(
            taskId=identifier.value,
            channelType=ChannelType.MAIL.value,
            requirement="test",
            because="help with development",
            state=TaskState.CREATED.value,
            attrs={"type_commit": CommitType.FIX.value},
        )
