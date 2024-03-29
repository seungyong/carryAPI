"""
    metaclass란?
    클래스를 관리하는 클래스이다.
    metaclass를 적용후 클래스를 만들면 metaclass에 __call__이 호출되어 해당 클래스를 컨트롤할 수 있다.
"""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:                                               # 인스턴스가 없다면
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)   # 인스턴스 생성 후 속성에 저장
        return cls._instances[cls]                                                  # 클래스로 인스턴스를 생성했으면 인스턴스 반환
