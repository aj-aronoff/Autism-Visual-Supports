# Gemini Gems — meta-prompt set

Eight meta-prompts, each beginning *"Write a great prompt to ..."*. Run each one in a
Gemini Gem; the Gem writes a prompt; that prompt is compared against the one in this
folder.

## The rule that keeps the comparison honest

**None of these meta-prompts contains my prompt, or any phrasing from it.** Each one
gives Gemini the same raw material I had — the job, the audience, the constraints, the
output shape — and nothing about how I solved it.

If a meta-prompt said "write a prompt that enforces a three-word label limit, positive
phrasing and a mandatory Then card," Gemini would hand back my prompt in its own
words, and the comparison would prove nothing. So the constraints are stated as
*facts about the problem* ("a child is matching a sound to a picture", "the parent has
four minutes") and the Gem has to derive the rules itself.

What to watch for when you compare: whether the Gem **derived a rule I missed**, and
whether it derived one of mine but **for a better reason**. Those are the two
outcomes worth copying. A Gem prompt that is merely longer is not better — length is
the usual failure of generated prompts, and on a metered token allocation it is a cost.

**Paste the responses here:** https://claude.ai/artifact/9J6JoXwVCY2Zd2bq3tSTh7

---

## 1. Composer

> Write a great prompt to turn a child's profile and a parent's description of a daily
> obstacle into a complete, ready-to-print visual support — the picture cards, the exact
> words the parent says out loud, and the instructions for using it.
>
> Context the prompt has to work inside. The user is the parent of an autistic child.
> They are not browsing; they are standing in a hallway with four minutes before they
> have to leave, and the same transition has gone badly every morning this week. They
> will read the result once, at speed, while holding a bag. The child is autistic and
> may be pre-verbal, an early reader, or a fluent reader. A visual support works because
> it is predictable: the child is learning to match a sound to a picture, so the words on
> the card and the words the parent says have to be the same words every time. Picture
> cards get printed, cut out, laminated and stuck to a fridge or a door at the child's
> eye level, and they get looked at by a child who is already upset.
>
> The thing being generated is one of four established formats: a two-card board pairing
> a non-preferred task with an immediate reward; a four-to-eight-card sequence for a
> multi-step routine; a one-to-three-card set communicating a boundary such as waiting or
> stopping; or a short illustrated narrative delivered days before an unfamiliar event.
> The prompt has to make the model choose between them rather than always producing the
> most elaborate one.
>
> This is a clinical-adjacent domain with a real literature behind it — these formats come
> from published autism intervention research, and the output is expected to name which
> established practice it rests on. It is also a domain where saying the wrong thing
> causes harm, and where some things a parent might describe are not visual-support
> problems at all and need a different response entirely.
>
> The output is consumed by software, not read as prose, and is validated before it is
> stored. Design the output shape accordingly.
>
> Write the prompt. Then list the decisions you made and why, so they can be argued with.

## 2. Reviewer

> Write a great prompt to review a draft visual support for an autistic child and return
> a structured verdict on whether it should be published, revised, or refused.
>
> Context. The draft was written by another AI model from a child's profile and a parent's
> description of a daily obstacle. It contains picture cards with short labels, a few
> phrases for the parent to say aloud, and instructions for using the support at home.
>
> The critical constraint: every countable rule has already been checked by ordinary
> code before this reviewer runs — word counts, number of cards, required fields present,
> a banned-word list. Those checks are deterministic and free. So the reviewer must not
> spend its judgement on anything a loop and an `if` statement can decide, and a prompt
> that has it re-counting words is a prompt that wastes a metered, monitored AI budget on
> arithmetic.
>
> What is left is everything a validator cannot reach. Some examples of the *kind* of
> thing, not a list to implement: whether a reward the draft promises is one the parent
> can actually produce in the next minute in their own house; whether the picture
> described actually depicts the thing its label names; whether the draft reaches for an
> elaborate format where a simple one would have been used and kept; whether the language
> treats the child as a person rather than as a behaviour to be managed. Work out the
> full set yourself from the situation.
>
> The reviewer has no tools and cannot edit the draft — it can only report. Consider why
> that separation might be deliberate, and let it shape the prompt.
>
> A reviewer that finds a problem every time stops being read. A reviewer that passes
> everything is decoration. The prompt has to land between those.
>
> The verdict is consumed by software: on one outcome the drafting model is called again
> with the findings attached, on another the draft is stored, on a third it is withheld.
> Design the output shape accordingly.
>
> Write the prompt. Then explain how you decided what belongs to the model and what
> belongs to the code.

## 3. Illustrator

> Write a great prompt to decide, for a single picture card in a visual support for an
> autistic child, whether a picture that already exists should be reused or a new one
> generated.
>
> Context. The card has a short label such as "Shoes" or "Wash hands". The system can
> search two pools of existing pictures: ones this particular child has used before, and
> a general starter set. It can also generate a new picture, which costs roughly a
> thousand times what a text decision costs, against an AI allowance that is capped and
> monitored.
>
> The thing that makes this more than a cost question: an autistic child using a visual
> support is learning that a particular picture means a particular thing. A new,
> slightly different, slightly better picture for something they already have a picture
> for does not improve the board — it damages it. Work out what that implies for how the
> decision should be weighted, and for what counts as "the same" picture when the labels
> differ in wording.
>
> When a new picture genuinely is needed, the prompt also has to specify what it should
> look like. The constraint is physical: it will be printed, cut to about two inches
> square, laminated, stuck to a door, and looked at by a child who is already distressed
> and may not read. Some children's profiles call for flat icons, some for simple line
> drawings, some for photographs, and some for no picture at all.
>
> The decision is consumed by software and must say which existing picture, or what to
> generate, or neither. Design the output shape accordingly.
>
> Write the prompt. Then say which parts of this decision you would not trust a language
> model with at all, and why.

## 4. Safety gate

> Write a great prompt to decide, from a parent's free-text description of a problem with
> their autistic child, whether the right response is a visual support or whether it is
> something else entirely — and to produce that something else when it is.
>
> Context. The parent typed a sentence or two into a box that asked what was going
> wrong. They are expecting to get a printable picture board back. Most of the time that
> is the correct thing to give them: trouble leaving the park, a fight about teeth, a
> dentist visit next week.
>
> Sometimes it is not. A parent describing a child who is hurting themselves, who ran
> into a road, who has not eaten in two days, or who is asking whether a medication is
> working, has not asked a visual-support question. Handing that parent a picture board
> is not a neutral non-answer — it implies the problem is the kind of problem a picture
> board addresses, and it costs them time they do not have. Work out the full set of
> cases yourself.
>
> The response in those cases has to be written for someone frightened, in plain words,
> short, without clinical vocabulary, without reassurance that is not earned, and without
> anything that reads as a diagnosis. It also has to avoid the opposite failure: refusing
> so broadly that an ordinary hard morning gets treated as an emergency, which teaches
> the parent that the tool is useless for the things it is actually for.
>
> The product is not a medical service and must not present itself as one. It also must
> not lecture.
>
> The output is consumed by software, which routes to one of two screens. Design the
> output shape accordingly.
>
> Write the prompt. Then describe the two ways it could fail and which one you optimised
> against.

## 5. Image prompt style

> Write a great prompt to convert a two-or-three-word card label into an image-generation
> prompt for a picture card used in a visual support for an autistic child.
>
> Context. The label is something like "Put on shoes", "Wash hands", "Wait", or "Swing".
> The picture produced from it will be printed, cut to roughly two inches square,
> laminated, and stuck to a door at a child's eye level. It will be looked at by a child
> who may not read, who may be pre-verbal, and who is frequently upset at the moment they
> look at it. Several of these cards sit side by side on one board and have to be
> distinguishable from each other at a glance, across a room.
>
> Some labels name an object. Some name an action. A few name an abstraction — waiting,
> stopping, a plan that changed. Those three are the hard ones and they recur on almost
> every board.
>
> The child's profile specifies one of four visual styles: flat icons, simple line
> drawings, photographs, or no picture at all. The prompt must handle all four.
>
> Two things are forbidden for reasons worth working out: the child's name must never
> reach the image model, and the picture must never contain text.
>
> The output of this prompt is fed directly to an image model, so it is a string, not a
> document.
>
> Write the prompt. Then explain how you handled the abstract labels, which is where this
> gets interesting.

## 6. Caregiver SMS

> Write a great prompt to turn a finished visual support into two text messages: one sent
> to the parent shortly before the routine happens, and one that asks them afterwards
> whether it worked.
>
> Context. The parent made a picture board for a daily transition. The board is on the
> fridge. The method only works if two things happen: the parent says the same few words
> each time, and the reward the board promises actually gets delivered. The second one is
> the one that quietly fails, and nobody will open an app to report that it failed.
>
> So the outbound message carries the words to say, at the moment they are needed, to
> someone who is holding a bag and a child. The reply message has to capture whether the
> reward was delivered and roughly how it went, from a parent who will answer with one
> word while walking, if they answer at all. The reply is parsed by software and written
> to a log, so the prompt has to decide what the parent is asked to send back and how
> forgiving the parsing has to be.
>
> Constraints worth reasoning about: a text message is charged per segment and read in a
> notification preview; this is a message about someone's child arriving on their phone
> in public; and a parent who finds the messages nagging will stop the whole thing, which
> ends the data as well as the support.
>
> There are also rules about automated messaging — consent, identifying the sender, and
> how someone stops the messages — that apply whether or not anyone mentions them.
>
> The output is consumed by software and must separate the two messages and the expected
> reply vocabulary. Design the output shape accordingly.
>
> Write the prompt. Then say what you would measure to know whether the reply message is
> working.

## 7. Intake wizard

> Write a great prompt to run a short conversation that collects everything needed to
> generate a visual support for an autistic child, in as few questions as possible.
>
> Context. The user is a parent. The information that produces a genuinely tailored
> result is substantial: the child's age and developmental stage, how they communicate,
> whether they read, what they are intensely interested in, what they are sensitive to,
> what sets them off, what the specific obstacle is, where it happens, and what reward
> actually motivates them.
>
> Asking all of that is a form the parent abandons. Most of it, though, is true about the
> child for years, while only a little of it changes from one board to the next. Work out
> what that implies for how the questioning should be split, and what can be inferred
> rather than asked.
>
> The parent is a world expert on this child and a novice at this vocabulary. A question
> using a term of art gets a blank or a wrong answer. A question that asks them to
> categorise their own child against a list they did not write feels like an assessment,
> and this parent has sat through a lot of assessments.
>
> The conversation also needs to end. A prompt that produces a warm, endless, empathetic
> interview has failed at the actual job, which is to get a printable board onto a fridge
> tonight.
>
> The collected answers are stored as structured records. Design the output shape
> accordingly.
>
> Write the prompt. Then state the smallest number of questions you think this can be
> done in, and what you gave up to get there.

## 8. Eval judge

> Write a great prompt to score a generated visual support for an autistic child against
> a reference version of the same support, so that two different prompt designs can be
> compared on the same test cases.
>
> Context. There is a set of test cases, each one a child profile plus a described
> obstacle. For each case a human expert has written what a good result looks like. Two
> candidate systems each generate a result. The scoring has to say which is better, on
> what dimension, and by enough of a margin to act on.
>
> The difficulty: the reference is one good answer, not the only one. A candidate that
> chose a different reward, a different theme, or different wording may be equally good or
> better, and a judge that scores similarity to the reference will reward imitation and
> punish improvement. But a judge with no reference at all drifts, rates everything
> highly, and prefers the longer answer. Work out how to get the discrimination without
> the imitation.
>
> What actually matters about these supports is not their wording. It is whether the
> format fits the obstacle, whether the reward is one the parent can really deliver, and
> whether the card, the spoken words and the picture all name the same thing. Those are
> not equally important and should not be weighted as if they were.
>
> The scores are compared across runs and stored, so they have to be stable enough that
> the same input twice does not move the number much.
>
> Write the prompt. Then say how you would check that the judge itself is any good.
