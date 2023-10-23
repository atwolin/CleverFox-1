import openai
import streamlit as st
from format import match_tokens_from_errant, print_double_space, submit_button, show_result
from streamlit import session_state


def find_nth_word(temp_word, n):
    if n <= len(temp_word):
        return temp_word[n]
    else:
        return None


def chat(prompt, text, tmpr, num_token):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": rf"{text}, {prompt}"},
        ],
        temperature=float(tmpr),
        max_tokens=int(num_token),
    )
    return response


def grammar(text):
    '''
    call ChatGPT to correct the text(article)
    '''
    temp_prompt = """Please do grammatical error correction task, don't change the architecture of the article. """
    # massenge
    submit_msg = submit_button()
    submit_prompt = st.button(submit_msg[session_state.submit_revise_query])
    result = show_result()
    st.subheader(result[session_state.submit_revise_query])
    # result
    if submit_prompt:
        # Get ChatGPT answer
        completion = chat(temp_prompt, text, 0.3, 500)
        response = completion['choices'][0]['message']['content']
        # Using errant to compare and produce edited articale
        fixed_sentence = match_tokens_from_errant(text, response)
        st.write(response)
        st.write(fixed_sentence)

        # Display double space format
        print_double_space(fixed_sentence)

        # Explanation
        getExplain(fixed_sentence)

        # Original fixed sentence
        with st.expander('Original Fixed Sentence'):
            st.write(response)
        # # All content of reponse
        # with st.expander('Whole Response'):
        #     st.write(response)


# explain
def getExplain(fixed_sentence):
    if session_state.submit_revise_query == "EN":
        return getExplain_en(fixed_sentence)
    if session_state.submit_revise_query == "TN":
        return getExplain_tn(fixed_sentence)
    if session_state.submit_revise_query == "JP":
        return getExplain_en(fixed_sentence)


def getExplain_en(fixed_sentence):
    # fixed_sentence = st.text_area('Fixed Sentence', f'{fixed_sentence}')
    QUES1 = "Compare EVERY modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : Last summer, I {+went+} [-go-] on a trip to {+a+} [-an-] beautiful beach. The weather {+was+} sunny and warm."
    ANS1 = "| Original Words | Replacement | Span of Words | Explanation |\n|---|---|---|---|\n|  go | went | I went on a trip | The change from \"go\" to \"went\" is made to correct the verb tense error. |\n| an | a | a beautiful beach | Because 'beautiful beach' starts with a consonant sound, you should use 'a' as the article, not 'an'. | N/A | was | The weather was | The original sentence lacks the auxiliary verb \"was,\" resulting in a missing verb between the subject \"the weather\" and the descriptive phrase \"sunny and warm.\" |"
    QUES2 = "Compare EVERY modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : I built {+sandcastles+} [-sendcastles-] with my family {+and+} [-or-] collected seashells."
    ANS2 = "| Original Words | Replacement | Span of Words | Explanation |\n|---|---|---|---|\n| sendcastles | sandcastles | built sandcastles | The original \"sendcastles\" is spelled incorrectly; the correct spelling is \"sandcastles.\" |\n| and | or | and collected seashells | The original use of \"or\" implies that you can only choose one activity, but based on the context, your intention is to do both activities simultaneously, so you need to use \"and\" to connect the two verbs. |"
    QUES4 = "Compare EVERY modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : Water shortage has been a serious problem for many years and {+has caused+} [-causes-] various crises."
    ANS4 = "| Original Words | Replacement | Span of Words | Explanation |\n|---|---|---|---|\n| causes | has caused | has caused various crises | To maintain tense consistency, we should use the past perfect tense \"had caused\" to express that this issue had already caused various crises over the years.|"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": QUES1},
            {"role": "assistant", "content": ANS1},
            # {"role": "user", "content": QUES3},
            # {"role": "assistant", "content": ANS3},
            {"role": "user", "content": QUES2},
            {"role": "assistant", "content": ANS2},
            {"role": "user", "content": QUES4},
            {"role": "assistant", "content": ANS4},
            {
                "role": "user",
                "content": f"Compare EVERY modified parts to the original text of the following setnece, precisly explain the replacement in a markdown table :{fixed_sentence}",
            },
        ],
        temperature=0,
        max_tokens=1500,
    )
    response_text = response["choices"][0]['message']['content']
    st.write('Below is the table of the explanation： \n', response_text)

    return response_text


def getExplain_tn(fixed_sentence):
    # fixed_sentence = st.text_area('Fixed Sentence', f'{fixed_sentence}')
    QUES1 = "Compare EVERY modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : Last summer, I {+went+} [-go-] on a trip to {+a+} [-an-] beautiful beach. The weather {+was+} sunny and warm."
    ANS1 = "| 原字詞 | 替代字詞 | 詞組(span of words) | 解釋 |\n|---|---|---|---|\n|  go | went | I went on a trip | 將\"go\"改為\"went\"是為了修正動詞的時態錯誤。 |\n| an | a | a beautiful beach | 由於 \"beautiful beach\" 以子音音素開頭，所以需要使用 \"a\" 這個冠詞，而不是 \"an\"。 | N/A | was | The weather was | 原句中缺少了 \"was\" 這個助動詞，這導致了句子的主詞 \"the weather\" 和描述詞片語 \"sunny and warm\" 之間的動詞缺失。|"
    QUES2 = "Compare EVERY modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : I built {+sandcastles+} [-sendcastles-] with my family {+and+} [-or-] collected seashells."
    ANS2 = "| 原字詞 | 替代字詞 | 詞組(span of words) | 解釋 |\n|---|---|---|---|\n| sendcastles | sandcastles | built sandcastles | 原本的 \"sendcastles\" 拼寫錯誤，正確的是 \"sandcastles\"。 |\n| and | or | and collected seashells | \原文使用的 \"or\" 暗示只能選擇其中一個活動，但根據上下文，你的意圖是同時進行兩個活動，所以需要使用 \"and\" 來連接兩個動詞。 |"
    QUES3 = "Compare EVERY modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : I am against the other product, {+the+} invisible cloaks."
    ANS3 = "| 原字詞 | 替代字詞 | 詞組(span of words) | 解釋 |\n|---|---|---|---|\n| N/A | the | the invisible cloaks | \"invisible cloaks\" 是特指的名詞片語，需要使用定冠詞 \"the\" 來指明你所提到的具體產品是哪一種。|"
    QUES4 = "Compare EVERY modified parts to the original text of the following setnece, precisly explain why the replacement is better than original word in a markdown table : Water shortage has been a serious problem for many years and {+has caused+} [-causes-] various crises."
    ANS4 = "| 原字詞 | 替代字詞 | 詞組(span of words) | 解釋 |\n|---|---|---|---|\n| causes | has caused | has caused various crises | 為了保持時態一致性，我們應該使用過去完成式 \"has caused\" 來表達這個問題已經對多年來造成的各種危機產生了影響。|"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": QUES1},
            {"role": "assistant", "content": ANS1},
            {"role": "user", "content": QUES3},
            {"role": "assistant", "content": ANS3},
            {"role": "user", "content": QUES2},
            {"role": "assistant", "content": ANS2},
            {"role": "user", "content": QUES4},
            {"role": "assistant", "content": ANS4},
            {
                "role": "user",
                "content": f"Compare EVERY modified parts to the original text of the following setnece, precisly explain the replacement in a markdown table :{fixed_sentence}",
            },
        ],
        temperature=0,
        max_tokens=1500,
    )
    response_text = response["choices"][0]['message']['content']
    st.write('以下為解釋表格： \n', response_text)

    return response_text
