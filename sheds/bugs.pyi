class BaseExceptionGroup(BaseException, Generic[_BaseExceptionT_co]):
    @overload
    def subgroup(
        self, __condition: type[_ExceptionT] | tuple[type[_ExceptionT], ...]
    ) -> ExceptionGroup[_ExceptionT] | None: ...