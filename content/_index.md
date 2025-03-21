---
# Leave the homepage title empty to use the site title
title: ""
date: 2022-10-24
type: landing

design:
  # Default section spacing
  spacing: "6rem"

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
      text: ""
      # Show a call-to-action button under your biography? (optional)
      button:
        text: Download CV
        url: uploads/resume.pdf
    design:
      css_class: dark
      background:
        color: black
        image:
          # Add your image background to `assets/media/`.
          filename: cherry-blossom.jpg
          filters:
            brightness: 1.0
          size: cover
          position: center
          parallax: false
  - block: markdown
    content:
      title: My Research
      subtitle: ''
      text: |-
        I am currently a Master's student in Computer Science at University of Illinois at Urbana-Champaign (UIUC), 
        supervised by [Professor Gokhan Tur](https://siebelschool.illinois.edu/about/people/department-faculty/gokhan) and [Professor Dilek Hakkani-Tür](https://siebelschool.illinois.edu/about/people/all-faculty/dilek). 
        Previously, I was an undergraduate student at New York University Shanghai, majoring in Computer Science and 
        minoring in Mathematics, supervised by 
        [Professor Yik-Cheung (Wilson) Tam](https://shanghai.nyu.edu/academics/faculty/directory/yik-cheung-wilson-tam).

        At New York University Shanghai, I conducted research on neural symbolic methods for boosting large language 
        models' reasoning ability and investigated the advantage of using Prolog langauge (a logic programming langauge) 
        as the generation output in terms of data augmentation for finetunining. After that, I explored how large language 
        models could be used to solve dialogua state tracking, which is a key component in task-oriented dialogues, and 
        witnessed a major improvement compared with previous methods.

        Now I have joined the ConvAI Lab at UIUC to explore the how large language models could reshape the form of 
        conversational AI. My research interest primarily lies in AI Agents and machine reasoning. If you are interested 
        in my research demonstrated below or would like to collaborate, please feel free to reach out to me 😃!
    design:
      columns: '1'
  - block: collection
    id: papers
    content:
      title: Featured Publications
      filters:
        folders:
          - publication
        featured_only: true
    design:
      view: article-grid
      columns: 2
  - block: collection
    content:
      title: Recent Publications
      text: ""
      filters:
        folders:
          - publication
        exclude_featured: false
    design:
      view: citation
  # - block: collection
  #   id: talks
  #   content:
  #     title: Recent & Upcoming Talks
  #     filters:
  #       folders:
  #         - event
  #   design:
  #     view: article-grid
  #     columns: 1
  - block: collection
    id: news
    content:
      title: Recent News
      subtitle: ''
      text: ''
      # Page type to display. E.g. post, talk, publication...
      page_type: post
      # Choose how many pages you would like to display (0 = all pages)
      count: 5
      # Filter on criteria
      filters:
        author: ""
        category: ""
        tag: ""
        exclude_featured: false
        exclude_future: false
        exclude_past: false
        publication_type: ""
      # Choose how many pages you would like to offset by
      offset: 0
      # Page order: descending (desc) or ascending (asc) date.
      order: desc
    design:
      # Choose a layout view
      view: date-title-summary
      # Reduce spacing
      spacing:
        padding: [0, 0, 0, 0]
  - block: cta-card
    demo: true # Only display this section in the Hugo Blox Builder demo site
    content:
      title: 👉 Build your own academic website like this
      text: |-
        This site is generated by Hugo Blox Builder - the FREE, Hugo-based open source website builder trusted by 250,000+ academics like you.

        <a class="github-button" href="https://github.com/HugoBlox/hugo-blox-builder" data-color-scheme="no-preference: light; light: light; dark: dark;" data-icon="octicon-star" data-size="large" data-show-count="true" aria-label="Star HugoBlox/hugo-blox-builder on GitHub">Star</a>

        Easily build anything with blocks - no-code required!
  
        From landing pages, second brains, and courses to academic resumés, conferences, and tech blogs.
      button:
        text: Get Started
        url: https://hugoblox.com/templates/
    design:
      card:
        # Card background color (CSS class)
        css_class: "bg-primary-700"
        css_style: ""
---
