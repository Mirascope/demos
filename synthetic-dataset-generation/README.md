---
title: 'Creating a synthetic dataset with Mirascope'
description: 'Using Mirascope to create a <Query, Response> dataset for finetuning an LLM for a CLI-Chatbot.'
---

### Background:
This demo uses Mirascope, and a series of models to generate a synthetic dataset. We will later use this dataset to help our LLM-based CLI tool Eddie get better at data visualization queries.

We want to generate a series of `<Query, Response>` pairs where the `Queries` are potential user queries that relate to using Matplotlib. These queries will have an emphasis on command-line situations. The `Responses` will be the resulting responses from a strong model to then fine-tune a much smaller model for Eddie.


### Strategy:
We'll generate synthetic queries with Task Templates. We'll start with just one query example. We will use Mirascope and LLMs to generate thousands of synthetic queries. 

To Generate Task Templates, we will describe a query generation process to a LLM and ask it to come up with samples of templated queries. We'll expand on these later by generating different data to fill the templates. We start with GPT-4 to generate our first examples (roughly 5), and GPT-4-Turbo for candidate values. We use these models instead of open source models because of the quality of their answers and reliability when doing structured extraction. Structured extraction lets us cleanly chain calls together in Mirascope.

We have queries with multiple templated variables plus lists of potential variables. We can substitute different combinations of the variables to scale to thousands of queries without using many tokens up front.

To generate the actual responses, we will use Mixtral hosted on Groq's API. This API is both free and very low latency. We have a lot of queries to process in sequence of each other, making this API perfect for us.

### Future steps:
We could increase the quality of the <Query,Response> dataset by increasing the number of generated template examples. This would increase the total number and diversity of examples, such that a random sampling will retain a more diverse query set.

We could also use a language model to refine, change, and expand these queries. This could be adding more specificity, or introducing other requirements. These queries could be higher in quality and therefore the tokens generated would be higher quality as well, leading to a downstream improvement in the resulting model. 

We will leave these as future work in case they are needed.





