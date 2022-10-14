# internal
from tier.internal.commit_analyzer import CommitAnalyzer
from tier.internal.versioning.bump_type import BumpType


def test_major_1():
    analyzer = CommitAnalyzer()
    msg = 'feat!: x'
    assert analyzer.analyze_message(msg) == BumpType.MAJOR


def test_major_2():
    analyzer = CommitAnalyzer()
    msg = 'feat: x\n\nBREAKING CHANGE: y'
    assert analyzer.analyze_message(msg) == BumpType.MAJOR


def test_major_3():
    analyzer = CommitAnalyzer()
    msg = 'feat!: x\n\nBREAKING CHANGE: y'
    assert analyzer.analyze_message(msg) == BumpType.MAJOR


def test_major_4():
    analyzer = CommitAnalyzer()
    msg = 'feat(component)!: x'
    assert analyzer.analyze_message(msg) == BumpType.MAJOR


def test_minor_1():
    analyzer = CommitAnalyzer()
    msg = 'feat: x'
    assert analyzer.analyze_message(msg) == BumpType.MINOR


def test_minor_2():
    analyzer = CommitAnalyzer()
    msg = 'feat(component): x'
    assert analyzer.analyze_message(msg) == BumpType.MINOR


def test_minor_3():
    analyzer = CommitAnalyzer()
    msg = 'feat: x\n\nextended message\n'
    assert analyzer.analyze_message(msg) == BumpType.MINOR


def test_patch_1():
    analyzer = CommitAnalyzer()
    msg = 'fix: x'
    assert analyzer.analyze_message(msg) == BumpType.PATCH


def test_patch_2():
    analyzer = CommitAnalyzer()
    msg = 'fix(component): x'
    assert analyzer.analyze_message(msg) == BumpType.PATCH


def test_patch_3():
    analyzer = CommitAnalyzer()
    msg = 'fix: x\n\nextended message\n'
    assert analyzer.analyze_message(msg) == BumpType.PATCH


def test_minor_and_patch():
    analyzer = CommitAnalyzer()
    msg1 = 'feat: x'
    msg2 = 'fix: x'
    assert analyzer.analyze_messages(msg1, msg2) == BumpType.MINOR


def test_major_and_minor():
    analyzer = CommitAnalyzer()
    msg1 = 'feat!: x'
    msg2 = 'feat: x'
    assert analyzer.analyze_messages(msg1, msg2) == BumpType.MAJOR
