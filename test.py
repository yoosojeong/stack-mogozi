import csv
import logging

from konlpy import jvm
from konlpy.tag import Twitter

logger = logging.getLogger(__name__)


def main():
    """
        konlpy 사용시 주의 사항
        자바 설치 및 세팅 필요
        JAVA_HOME 세팅이 필요합니다.
        export JAVA_HOME=$(/usr/libexec/java_home)
    """
    konl = Twitter()
    test_string = [
        u'konlpy 사용시 주의 사항',
        u'자바 설치 및 세팅 필요',
        u'JAVA_HOME 세팅이 필요합니다.',
        u'export JAVA_HOME=$(/usr/libexec/java_home)',
    ]
    for row in test_string:
        r = konl.pos(row, norm=True, stem=True)
        print('=' * 20)
        for txt, post in r:
            print(txt, post)
        print('=' * 20)


if __name__ == '__main__':
    jvm.init_jvm()
    main()
