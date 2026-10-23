# Autism Visual Supports

**First → Then boards that parents can print, post, and trust.**

Repository: https://github.com/aj-aronoff/Autism-Visual-Supports

---

## The problem

Ask any parent of an autistic child about mornings and you will hear the same story.
The child is on the floor with a toy. In four minutes they need shoes on with their
go-bag and they need to be in the car. "We have to go now" does not work, and saying
it louder works less.

What works is a picture. **First shoes. Then swing.** Two cards, in order, where the
child can see them.

The method is not in question. The Vanderbilt Kennedy Center's TRIAD toolkit,
published through the Autism Speaks Autism Treatment Network, documents First–Then
boards, visual schedules and parameter cards as core practice. The National Autism
Center's *National Standards Report* lists Schedules, Antecedent Packages and
Story-based Intervention among the interventions with compelling scientific evidence.

What fails is the **making**. A good board means finding pictures the child
recognises, cutting them to size, keeping every label to three words or fewer,
laminating, and adding Velcro. That is a forty-minute craft project, and the morning
you needed it was this morning. Most parents make two or three boards, ever, and then
stop.

And there is a second failure, quieter and worse. The toolkit is blunt about it:

> *"In order to teach children with ASD the value of the First-Then Board, you must
> give them the reinforcing activity or item after they complete the 'first' task.
> Otherwise, your child may not trust the board the next time you use it."*

A board the child has stopped trusting is not a neutral outcome. It is worse than no
board, because the next one starts from suspicion.

## The solution

A web application on OutSystems Developer Cloud where a parent answers three
questions and has a complete, usable visual support in under two minutes.

**Three questions.** Which routine. What is hard about it. What the child actually
wants afterwards. The child's profile — age, whether they read, whether they prefer
photographs or simple icons, their special interests, their sensory triggers — is
filled in once and reused forever.

**Three things come back**, because the research says the picture alone is not enough:

1. **The cards** — correctly sized, three words maximum per label, phrased positively
   ("Walk in hallway", never "Don't run"), ready to print with cut lines for
   lamination or to use full-screen on a tablet.
2. **The caregiver script** — the one or two low-demand phrases to say out loud.
   *"First shoes, then swing."* Then afterwards, *"All done shoes. Now swing!"* Most
   tools stop at the picture. The words are what parents fumble.
3. **The implementation plan** — where to put the board, the prompt hierarchy from
   least to most intrusive, and what to do when it goes wrong.

**And then the part nobody else does.** When the routine is due, the app texts the
parent the script. Afterwards it asks one question: *did the reward actually happen?*
The reply is one character.

That single field is the one the entire method depends on, and the one no parent will
ever open an app to fill in — because at that moment they are at the front door
holding a pair of shoes, not a tablet. The home screen shows, per board, how reliably
the promise has been kept. Not how many boards you have made.

## How it is built

**OutSystems Developer Cloud** for the application, data model, user management, and
both outputs — print sheet and tablet mode — from one definition.

**Agentic AI**, as an orchestrated workflow in Agent Workbench rather than a single
prompt. Three agents, each with a job small enough to inspect:

- **Composer** reads the child's profile and the obstacle, chooses the support type,
  and drafts the cards, script and plan against a grounded knowledge source — the
  TRIAD toolkit and the National Standards Report. Every board names the
  evidence-based practice it rests on.
- **Reviewer** checks that draft against the design rules and sends it back when it
  drifts: labels over three words, negative phrasing, a missing reward card, too many
  steps for the child's developmental stage.
- **Illustrator** searches the child's existing card library before generating
  anything new, so "brush teeth" keeps the same picture forever. Predictability is
  not a nice-to-have here; it is the product.

**Twilio** carries the script and the reward question by SMS — the only channel that
reaches a parent mid-routine.

**Guardrails are enforced in the application, not requested in a prompt.** Labels over
three words are rejected. A First–Then board cannot be saved without a Then card.
When a parent describes self-injury or escalation, the app does not generate a board —
it says so plainly and surfaces referral guidance instead. No diagnosis, no clinical
advice, and a child's name never appears in an image prompt.

## Who it is for

Parents first. Then the teacher, the aide and the speech-language pathologist, who can
be given read-only access to the same boards — because the toolkit is clear that
visual supports work best when the same pictures follow the child across every
setting.

## Where the project stands

Pre-build, by design: ODC access opens only after registration closes, so the
application itself is built during the 2–9 November window.

**Already done and in the repository:**

- The full build specification — nine entities, eight screens, the three-agent
  workflow, the JSON output contract and seven guardrails (`SPEC.md`)
- A project deck, as PowerPoint and PDF (`docs/`)
- The complete artwork set, every image original vector art generated from source,
  with the palette and design rules documented (`assets/`)
- The three prompt drafts the pipeline was derived from (`prompts/`)

**During the build week**, in this order: entities and child profile → Composer and
Reviewer on the First–Then branch → the three-question wizard → Illustrator and the
card library → print sheet and tablet mode → the Twilio loop and the trust streak →
a UX pass → the demo video.

One support type, end to end, before any second one. A First–Then board that
generates, prints, goes on a fridge, texts the parent and records the reward is a
complete demonstration. Four half-built tool types are not. Visual schedules,
parameter cards and social narratives are the roadmap, not the seven days.

## Why this team

My daughter is autistic. My wife will be the first test user. I have been making these
boards by hand for years, and I know exactly which forty minutes this application
gives back.

## Nonprofit partner

Autism Speaks, whose Autism Treatment Network published the visual supports toolkit
this work is built on. We are also pursuing an introduction to TRIAD at the Vanderbilt
Kennedy Center and to local Autism Society chapters, where a 12-month ODC licence
would go furthest.

---

*Built for the OutSystems Build for the Future Hackathon 2026. Open source under MIT,
per the hackathon rules.*

*Evidence base: Vanderbilt Kennedy Center TRIAD / Autism Speaks ATN, "Visual Supports
and Autism" (2011); National Autism Center, "National Standards Report" (2009).*
