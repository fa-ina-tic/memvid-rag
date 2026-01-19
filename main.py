from memvid_sdk import create, use


if __name__ == "__main__":
    with use("basic", "knowledge.mv2", mode="auto", enable_vec=True, read_only=True) as mv:
        stat = mv.stats()
        answer = mv.ask(
            'Qualcomm',
            mode='hybrid'
        )