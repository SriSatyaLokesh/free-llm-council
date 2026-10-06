"""
Prompts for the four council stages.

Kept in one place so the wording of each stage can be reviewed and tuned
without touching orchestration code.
"""

# The persona every council member carries in every stage. It is prepended to
# each prompt rather than baked into an opencode agent, because opencode 2.0.18
# silently fails to run custom agents declared in a project-level config.
COUNCIL_MEMBER_PREAMBLE = """You are one member of an LLM Council. Several other \
AI models are working on the same question alongside you, in parallel, and you \
will later read what they say.

How you should work:
- Form your own view first. Do not try to guess what the others will say, and do \
not hedge for its own sake.
- Ground your answer in evidence. You have webfetch and websearch available, and \
you may read files in the workspace. Use them whenever the question depends on \
facts, current information, or specifics you are unsure about. Cite what you \
actually looked up. If you did not verify something, say so plainly instead of \
inventing detail.
- Be concrete. Vague agreement helps nobody.
- Always make the tradeoffs explicit: what your view gives up, what it risks, and \
under what circumstances you would choose differently.
- Be concise. You are one voice among several, not the final authority."""


CAVEMAN_PREAMBLE = None  # superseded by backend.caveman.build_instruction()


def position_prompt(user_query: str, model_name: str) -> str:
    """Stage 1: independent first opinion. Never compressed - a human reads this."""
    return f"""{COUNCIL_MEMBER_PREAMBLE}

---

The other council members are answering independently right now. You will not \
see their answers until the debate stage, so give the answer you would defend.

QUESTION FROM THE USER:
{user_query}

Write your position on this question. Structure it as:
1. Your recommendation, stated plainly and up front.
2. The reasoning that supports it, with evidence. If you looked anything up, say what.
3. The tradeoffs: what this costs, what it risks, who it is wrong for.
4. What would change your mind.

You are {model_name}. Answer in your own voice."""


def debate_prompt(
    user_query: str,
    your_model: str,
    positions_text: str,
    prior_rounds_text: str,
    round_number: int,
    total_rounds: int,
    caveman_instruction: str = None,
    human_guidance: list = None,
) -> str:
    """
    Stage 2: named cross-examination, one round at a time.

    `caveman_instruction` is the official Caveman text (see backend.caveman).
    When it is present the model-to-model exchange is compressed and the
    scaffolding that exists only for a human reader is dropped. The debate
    contract itself - rebut a named peer, concede what moved you, say
    UPDATING or DEFENDING, raise a missed tradeoff - is identical either way.
    `human_guidance` provides injected mid-debate steering directives and resources.
    """
    compressed = bool(caveman_instruction)

    guidance_block = ""
    if human_guidance:
        lines = []
        for g in human_guidance:
            msg = g.get("message", "").strip()
            res = g.get("resources", [])
            res_str = f" [Resources: {', '.join(res)}]" if res else ""
            lines.append(f"- {msg}{res_str}")
        formatted_guidance = "\n".join(lines)
        guidance_block = f"""

[HUMAN OPERATOR GUIDANCE & STEERING]
{formatted_guidance}
MANDATORY DIRECTIVE: All council members must address and align their arguments with this guidance in subsequent debate rounds."""

    if round_number == 1:
        round_context = (
            "This is the opening round. There is no debate transcript yet, so "
            "these are the members' opening positions."
        )
        section_header = "OPENING POSITIONS:"
        body = positions_text
    else:
        round_context = "Here is the debate transcript so far:"
        section_header = "DEBATE SO FAR:"
        body = prior_rounds_text

    remaining = total_rounds - round_number
    closing = (
        "\nThis is the final round. The Chairman reads the transcript after this, "
        "so make sure your final position and your strongest objections are on the "
        "record."
        if remaining <= 0
        else f"\n{remaining} more round(s) will follow, so leave room to be persuaded."
    )

    # In compressed mode the persona block is replaced wholesale: it is written
    # for a human reader and is the single largest block of instruction text in
    # the prompt. The debate contract below carries the same requirements.
    header = caveman_instruction if compressed else COUNCIL_MEMBER_PREAMBLE

    if compressed:
        return f"""{header}

---

ROUND {round_number} of {total_rounds}.

QUESTION: {user_query}
YOU: {your_model}

{section_header}
{body}{guidance_block}

Contract, unchanged by compression:
1. Rebut at least one peer by name. Name the weakest one. Be specific about what
   it gets wrong or overlooks.
2. Concede anything you are genuinely convinced by, and say what changed your mind.
3. State whether you are UPDATING or DEFENDING your position.
4. Raise the tradeoff the council is most likely to overlook.
{closing}"""

    return f"""{header}

---

{round_context}

{section_header}
{body}{guidance_block}

---

The original question the user asked:
{user_query}

You are {your_model}. It is your turn, round {round_number} of {total_rounds}.

Do all of the following in your reply:

1. Rebut at least one other member **by name**. Pick the one whose position is \
weakest and say specifically what it gets wrong or overlooks. Do not review all of \
them politely - that is not useful to anyone.

2. Concede anything you are genuinely convinced by. If a peer's argument changed \
your mind, say so plainly and say what changed it. Defending a position you have \
been persuaded off is the worst thing you can do here.

3. State whether you are UPDATING or DEFENDING your position, and why.

4. Raise the tradeoff you think the council is most likely to overlook.

{closing}

Be direct and specific. Reference members by their exact names as given above."""


def review_prompt(
    user_query: str,
    positions_text: str,
    label_to_model: dict,
    caveman_instruction: str = None,
) -> str:
    """Stage 3: blind, anonymized scoring of the positions."""
    labels = ", ".join(sorted(label_to_model.keys(), key=lambda k: k[-1]))

    if caveman_instruction:
        # Same task, compressed. The ranking format is a hard contract and is
        # restated verbatim, because a model that misses it contributes
        # nothing to the aggregate.
        return f"""{caveman_instruction}

---

QUESTION: {user_query}

ANSWERS (identities hidden on purpose - judge the work, not the name):
{positions_text}

Do this:
1. For each answer: one line, what it does well, one line what it does poorly.
2. Then rank them on correctness, whether claims are actually supported, depth
   of reasoning, usefulness to someone who must act on this, and honesty about
   uncertainty.

OUTPUT FORMAT - parsed by a script, follow exactly:
- A line containing exactly: FINAL RANKING:
- Then a numbered list, best first, one per line.
- Each line: number, period, space, then only the label. Example: "1. Response B"
- Nothing after the ranking list.

Valid labels: {labels}"""

    return f"""You are evaluating the answers several models gave to a question. \
Their identities are hidden from you on purpose, so that you judge the work rather \
than the reputation of whoever wrote it. Judge only what is in front of you.

QUESTION:
{user_query}

ANSWERS (anonymized):
{positions_text}

Your task:
1. Evaluate each answer individually. For each one, state what it does well and \
what it does poorly. Be specific - refer to the actual content, not to how it \
reads.
2. Then rank them.

Rank on: correctness, whether claims are actually supported, depth of reasoning, \
usefulness to someone who has to act on this, and honesty about uncertainty.

OUTPUT FORMAT - this part is parsed by a script, so follow it exactly:
- Start a line containing exactly: FINAL RANKING:
- Then a numbered list, best first, one per line.
- Each line is: number, period, space, then only the label. Example: "1. Response B"
- Put nothing after the ranking list.

Valid labels are: {labels}

Example of the required ending:

FINAL RANKING:
1. Response C
2. Response A
3. Response B"""


def verdict_prompt(
    user_query: str,
    positions_text: str,
    debate_text: str,
    review_text: str,
    aggregate_text: str,
    chairman_model: str,
    debate_was_compressed: bool = False,
    compression_modes: str = "",
    human_guidance: list = None,
) -> str:
    """Stage 4: the chairman's decision. Never compressed - a human reads this."""
    if debate_was_compressed:
        compression_note = f"""

NOTE ON STAGE 2: the debate above was run in compressed mode ({compression_modes}) \
to save tokens. Members were terse, abbreviated, and dropped politeness. Do not \
reproduce that register. This is the one output a human actually reads, and you \
are now writing the report. Expand: restore the full reasoning behind each \
claim, spell out what each member meant, and supply the context that terse \
turns left out. A compressed transcript is a claim, not a conclusion - if a \
compressed turn is too thin to judge, say which one and why rather than \
silently inheriting it."""
    else:
        compression_note = ""

    guidance_section = ""
    if human_guidance:
        lines = []
        for g in human_guidance:
            msg = g.get("message", "").strip()
            res = g.get("resources", [])
            res_str = f" [Resources: {', '.join(res)}]" if res else ""
            lines.append(f"- {msg}{res_str}")
        formatted_guidance = "\n".join(lines)
        guidance_section = f"""

[HUMAN OPERATOR GUIDANCE & STEERING]
{formatted_guidance}

DIRECTIVE TO CHAIRMAN: The human operator injected direct steering guidance during the debate. Explicitly highlight how the final verdict aligns with or addresses the operator's input and resources."""

    return f"""You are the Chairman of an LLM Council. Several models have given \
independent answers to a user's question, debated each other over multiple rounds, \
and then scored each other's positions anonymously. You have read everything.{compression_note}{guidance_section}

ORIGINAL QUESTION:
{user_query}

STAGE 1 - OPENING POSITIONS:
{positions_text}

STAGE 2 - DEBATE TRANSCRIPT:
{debate_text}

STAGE 3 - BLIND PEER SCORING:
{review_text}

AGGREGATE SCORE (average rank across reviewers, lower is better):
{aggregate_text}

You are {chairman_model}. Produce the council's final answer.

You are not a summarizer. Several models here were wrong, and the aggregate scores \
are evidence, not a verdict - a single confident-sounding model is sometimes simply \
confident and wrong. Decide.

Use exactly these headings, in this order:

## Decision
The council's answer, stated directly. Do not hedge, and do not describe the \
process instead of answering. If the question is a design decision, commit to one.

## Reasoning
Why this is the right call. Cite which members' arguments carried the most weight \
and which evidence mattered. Name what actually decided it.

## Tradeoffs
What this decision gives up, what it costs, and who it is wrong for. Include the \
option that was rejected and why. If the council traded correctness against cost, \
speed against thoroughness, or safety against capability, say so explicitly.

## Dissent
Views that did not win but have real merit, and the condition under which you \
would switch to them. If the council was actually split, say so.

## Confidence
High, medium, or low - and the specific reason. Say what new information would \
move you, and what you are least sure about."""

VERDICT_SECTIONS = ("Decision", "Reasoning", "Tradeoffs", "Dissent", "Confidence")


def parse_verdict(text: str) -> dict:
    """
    Split a chairman response into its sections.

    Falls back to putting everything in 'Decision' if the headings are missing,
    so a non-compliant chairman still produces a usable answer.
    """
    import re

    if not text:
        return {section.lower(): "" for section in VERDICT_SECTIONS}

    pattern = r"^#{1,3}\s*(" + "|".join(VERDICT_SECTIONS) + r")\s*$"
    matches = list(re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE))

    if not matches:
        return {
            **{section.lower(): "" for section in VERDICT_SECTIONS},
            "decision": text.strip(),
        }

    sections: dict = {section.lower(): "" for section in VERDICT_SECTIONS}
    for index, match in enumerate(matches):
        key = match.group(1).lower()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[key] = text[start:end].strip()

    return sections


def title_prompt(user_query: str) -> str:
    """Short conversation title."""
    return f"""Generate a very short title (3-5 words maximum) that summarizes \
the following question. Concise and descriptive, no quotes and no punctuation.

Question: {user_query}

Title:"""
