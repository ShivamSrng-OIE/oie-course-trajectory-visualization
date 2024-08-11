# GemInCourse

**GemInCourse** is a course recommendation platform powered by Google's Gemini. It leverages the advanced capabilities of Gemini to comprehend undergraduate student queries and deliver precise, meaningful responses. Combined with a 3D interactive course track visualization feature, GemInCourse provides enhanced clarity on course options, highlighting the complexities associated with prerequisites and corequisites.

Link to the website: [*GemInCourse*](https://gemincourse.onrender.com/)

## Installation and Usage
```bash
# Cloning a specific branch of the repository:
git clone -b course-recommendation-chat git@github.com:ShivamSrng-OIE/oie-course-trajectory-visualization.git

# Changing the current directory:
cd .\oie-course-trajectory-visualization\


# Using package manager install the required libraries:
pip install -r .\requirements.txt

# After successful installation of all the packages, run the codebase using:
python app.py
```

## Project Overview and Development
1. Initially, we obtained the data by scraping the official website of the New Jersey Institute of Technology. The codebase for this process can be viewed here: [NJIT Course Catalog Scraper](https://github.com/ShivamSrng-OIE/njit-course-catalog-scrapper). This tool leverages Gemini's capabilities to automatically extract and segregate prerequisites, corequisites, and other relevant prerequisite information from the full course descriptions, formatting the final output appropriately.
2. The scraper is designed to handle API limitations efficiently, pausing for 2 minutes after every 10 API calls to Gemini to prevent issues related to **RESOURCES EXHAUSTED**. However, we are currently encountering a **RECITATION** error, which consistently occurs when processing specific courses. For example, the [logfile.json](https://github.com/ShivamSrng-OIE/njit-course-catalog-scrapper/blob/main/logfile.json) contains detailed logs of errors related to **RECITATION**, along with links to the course information where these errors were encountered.
3. All of the scraped data is stored in a MongoDB database, and the code for uploading this data to MongoDB is also included in the [NJIT Course Catalog Scraper](https://github.com/ShivamSrng-OIE/njit-course-catalog-scrapper) repository. To execute the codebase in this repository, please follow the instructions provided in its README file.
4. The 3D Course Trajectory graphs and the frontend (currently optimized for laptop and desktop screens) are developed using the **Dash** library in Python. Details of the features of the 3D course trajectory graph are discussed in the upcoming section
5. Interaction with Gemini begins when the 3D course trajectory graph is accessed in fullscreen mode via the button located at the bottom-left corner. This section handles the understanding of the undergraduate student's queries and performs tasks accordingly. Details of this functionality are discussed in the upcoming section.
6. The execution of the codebase begins with the [app.py](https://github.com/ShivamSrng-OIE/oie-course-trajectory-visualization/blob/course-recommendation-chat/app.py) file. The filenames within the directory are descriptive and intuitive. Comprehensive comments are provided throughout the code to enhance understanding of complex sections. Additionally, each class and its methods include docstrings that explain their purpose and functionality.

## Features
3D Course Trajectory Graph Overview:
1. **Interactive Course Nodes**: The graph features interactive course nodes. When a course node is clicked, the edges connecting to courses where the selected node serves as a prerequisite or corequisite are highlighted.
2. **Color-Coded Edges**: The color of the highlighted edges indicates the type of dependency. A yellow edge signifies that the clicked course is a corequisite, while a light blue edge shows that the clicked course is a prerequisite for the connected node.
3. **Critical/Gateway Courses**: Some nodes appear larger than others, representing critical or gateway courses. These courses are essential for undergraduate students to complete their degree track successfully, as they serve as prerequisites or corequisites for multiple other courses.
4. **Concentric Circle Towers**: The graph consists of two concentric circle towers. The main tower represents the undergraduate student's course trajectory to obtain the degree, while the Pre-Knowledge Courses tower displays courses that, while not taught at the university, are prerequisites or corequisites for courses within the degree program. Visualizing these courses is crucial for undergraduate students.
5. **Toggle Functionality**: Course nodes function as toggle buttons. Clicking a node again will de-highlight the corresponding edges.
6. **Hover Descriptions**: Hovering over course nodes reveals the course description without requiring a click or further interaction.
7. **Critical Course Dependencies**: Hovering over critical courses also displays a dependency count, indicating the number of subsequent courses for which the critical course is a prerequisite or corequisite.

Capability of Google's Gemini Chat Interaction:
1. **Robust Query Handling**: The system is designed to comprehend and respond effectively to undergraduate student queries, including those that may appear nonsensical.
2. **3D Graph Familiarization**: Undergraduate students can easily familiarize themselves with the visual details of the 3D graph by querying phrases such as "Provide information about the 3D graph," "Explain the details in the graph," or similar requests.
3. **Integrated Trajectory Planning**: The integration of Google's Gemini-powered chat with the 3D visualization allows undergraduate students to plan their academic trajectory towards a specific course within their track. The chat interface provides comprehensive information on all prerequisites and corequisites that must be completed in prior semesters to pursue the target course.
4. **Detailed Course Information**: Within the track, Google's Gemini offers in-depth information about each course, including course code, course name, prerequisites, corequisites, descriptions of prerequisites (with any grade requirements), course description, credit hours, contact hours, and a direct link to the course information on the New Jersey Institute of Technology's course catalog website.
5. **Course Recommendation System**: A key feature of this system is the course recommendation engine, currently tailored to the course offerings at the New Jersey Institute of Technology (NJIT). This approach ensures data integrity, as no unauthorized scraping from other institutions has been conducted. The recommendation engine leverages Gemini's capabilities to collect essential information from undergraduate students, making the system both relevant and accessible. Before generating recommendations, the system inquires about:
    - The **year** and **semester** for which the undergraduate student seeks course recommendations.
    - The **undergraduate student's career goals and aspirations**.
    - Whether the undergraduate student prefers a more **academically focused track** or one with **exposure to industrial experience**, such as CO-OP programs or internships, which make the track more applied and experience-based.


## Importance and Impact
1. **Secondary Academic Advisor**: Universities often refrain from disclosing the results of internal surveys regarding undergraduate student satisfaction due to confidentiality concerns. However, having personally encountered challenges related to course selection, this project aims to address these issues by offering a course recommendation service and additional features tailored to assist undergraduate students, effectively serving as a secondary academic advisor.
2. **Higher Satisfaction among Students**: The integration of such a tool within universities is expected to lead to a significant improvement in overall positive responses in student satisfaction surveys which at the end uplifts the ranking of the universities and attracts more students.
3. **Student's Benefits**: For students, this tool not only alleviates confusion surrounding course selection but also minimizes the risk of course dropouts caused by excessive academic pressure. By meticulously analyzing student-specific data, the enhanced version of the system (described in the upcoming section) can recommend a balanced mix of simpler and more challenging courses, thereby improving the overall academic experience. Additionally, the 3D course trajectory visualization simplifies the understanding of complex course prerequisites and corequisites, highlighting critical or gateway courses to students, making their academic planning more intuitive and manageable.
4. **University Benefits**: The integration of this tool will streamline the responsibilities of graduate advisors by automating and simplifying course recommendation processes. This efficiency will not only reduce the administrative burden on advisors but also enhance the overall relationship between the university and its students. By providing personalized and well-informed course recommendations, the tool fosters a more supportive academic environment, potentially leading to increased student satisfaction and retention of students within the particular course.


## Planned Enhancements
The following enhancements are designed with the specific needs of undergraduate students at the New Jersey Institute of Technology (NJIT) in mind. These enhancements consider that not all universities maintain comprehensive data across all areas, and are thus tailored for NJIT:
1. **Integration of Undergraduate Student Grades**: Incorporating the grades of courses that a undergraduate student has completed to refine course recommendations. For instance, if a undergraduate student has excelled in a prerequisite course, the system can identify and recommend courses with similar content, as the undergraduate student is likely to have a higher interest in those areas.
2. **Pass/Fail Ratio Analysis**: Incorporating pass and fail ratios for courses to highlight those that are particularly challenging for undergraduate undergraduate students. Based on this analysis, we plan to offer course recommendations that balance simpler and more complex courses within a semester, ensuring a manageable yet rigorous academic experience.
3. **Alumni Data Integration**: Integrating data about NJIT alumni, including their skills and current industry roles. By understanding their career paths, the system can provide recommendations that include collaborative filtering. If a undergraduate student’s career goals align with those of an alumnus who is thriving in that field, the recommendation system, powered by Gemini, will semantically match course descriptions to recommend those that align with the skills possessed by the alumni. The overall aim is to create a hybrid recommendation system.
4. **Advanced Interface for Undergraduate Advising**: Developing an advanced interface for NJIT’s Undergraduate Advising team, enabling them to easily add additional data to the course catalog. By simply providing course descriptions, the system—using Gemini—will automatically extract and segregate prerequisites, corequisites, and other related information, minimizing manual work and enhancing data accuracy.
5. **Advanced Student Query Handling**: Currently, Gemini is trained to respond to four specific types of undergraduate student queries. In the future, we are planning to enhance the system by granting Gemini access to a significantly larger dataset. This will enable Gemini to respond to a broader range of undergraduate student queries, including those that fall outside the current scope.
6. **The Graduate Students**: In the near future, we are planning to incorporate even the graduate course catalog data in the application. As a result the application will be able to even recommend courses to graduate student and resolve their queries.

## Contributors
* **Shivam Manish Sarang**
  - Graduate Student Research Assistant, for Office of Institutional Effectiveness.
  -  Currently pursuing Master's in Computer Science, Ying Wu College of Computing at New Jersey Institute of Technology.
  - Contact: [Shivam NJIT Email ID: sms323@njit.edu](mailto:sms323@njit.edu)
* **Yi Meng**
  - Associate Director for Survey Research, for Office of Institutional Effectiveness.
  - Contact: [Yi Meng NJIT Email ID: yi.meng@njit.edu](mailto:yi.meng@njit.edu)
* **Office of Institutional Effectiveness** - New Jersey Institute of Technology