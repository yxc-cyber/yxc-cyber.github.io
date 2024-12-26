---
title: 'Arithmetic Reasoning with LLM: Prolog Generation & Permutation'
authors:
- Xiaocheng Yang
- Bingsen Chen
- Yik-Cheung Tam
date: '2024-06-01'
publishDate: '2024-12-26T08:43:15.281869Z'
publication_types:
- paper-conference
publication: '*Proceedings of the 2024 Conference of the North American Chapter of
  the Association for Computational Linguistics: Human Language Technologies (Volume
  2: Short Papers)*'
doi: 10.18653/v1/2024.naacl-short.61
abstract: Instructing large language models (LLMs) to solve elementary school math
  problems has shown great success using Chain of Thought (CoT). However, the CoT
  approach relies on an LLM to generate a sequence of arithmetic calculations which
  can be prone to cascaded calculation errors. We hypothesize that an LLM should focus
  on extracting predicates and generating symbolic formulas from the math problem
  description so that the underlying calculation can be done via an external code
  interpreter. We investigate using LLM to generate Prolog programs to solve mathematical
  questions. Experimental results show that our Prolog-based arithmetic problem-solving
  outperforms CoT generation in the GSM8K benchmark across three distinct LLMs. In
  addition, given the insensitive ordering of predicates and symbolic formulas in
  Prolog, we propose to permute the ground truth predicates for more robust LLM training
  via data augmentation.
links:
- name: URL
  url: https://aclanthology.org/2024.naacl-short.61
---
