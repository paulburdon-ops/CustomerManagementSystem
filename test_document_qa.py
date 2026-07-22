from services.document_qa_service import (
    answer_morrisons_question,
)


def main() -> None:
    questions = [
        "What database does Sage X3 use?"
    ]

    for question in questions:
        print()
        print(f"Question: {question}")

        answer = answer_morrisons_question(question)

        print(f"Answer: {answer}")
        print("-" * 60)


if __name__ == "__main__":
    main()