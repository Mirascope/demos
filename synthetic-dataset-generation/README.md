---
title: 'Creating a synthetic dataset with Mirascope'
description: 'Using Mirascope to create a <Query, Response> dataset for finetuning an LLM for a CLI-Chatbot.'
---

### Background:
We're looking to generate a synthetic dataset, particularly to help our LLM-based CLI tool Eddie get better at data visualization queries.

We want to generate a series of `<Query, Response>` pairs where the `Queries` are potential user queries that relate to using Matplotlib, with an emphasis on command-line situations. The `Responses` will be the resulting responses from a strong model to then fine-tune a much smaller model for Eddie.


### Strategy:
We'll generate synthetic queries with Task Templates. We'll start with just one query example and with LLM's and some insight, we'll generate thousands of synthetic queries.

To Generate Task Tamples, we will describe query generation process to a Language model and ask it to come up with samples of templated queries, which we can use to expand later by generating different data to fill the templates. We will start with GPT-4 generate our first examples (roughly 5), and GPT-4-Turbo.

To generate the actual responses, we will use Mixtral hosted on Groq's API, which is free at the time of writing, and we have a decent amount of tokens to process.

### Future steps:
We could increase the quality of the <Query,Response> dataset by increasing the number of generated template examples. This would increase the total number of examples, but also the diversity, such that a random sampling will retain a more diverse query set.

We could also use a language model to refine, change, and expand these queries. This could be adding more specificity, or introducing other requirements. These queries could be higher in quality and therefore the tokens generated would be higher quality as well, leading to a downstream improvement in the resulting model. 

We will leave these as future work in case they are needed.





