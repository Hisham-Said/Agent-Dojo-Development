# main.py

from agent.llm_agent import LLMAgent


def main():

    agent = LLMAgent()

    # result = agent.run(
    #     "Read my emails and summarize them."
    # )
    # result = agent.run("What meetings are on my calendar?")
    # result = agent.run("Find my project report.")
    result = agent.run("Read my project report and summarize it.")

    print("\n==============================")
    print("FINAL ANSWER")
    print("==============================")
    print(result)


if __name__ == "__main__":
    main()