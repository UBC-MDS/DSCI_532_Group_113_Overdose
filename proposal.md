## Proposal
### Section 1: Motivation and Purpose
According to recent article published by the journal of Drug and Alcohol Dependence<sup>[1]</sup>, Connecticut, U.S has suffered from a sever escalation in overdose deaths in the period between 2012 and 2018. This has prompted the attention of health professional and public policy makers and research institutions to understand the roots of this issue.

To contribute to the effort toward the prevention of accidental death overdose in Connecticut, we are proposing a data visualization app that will assist the health professional, public policy makers and research institutions to identify the people who are most vulnerable to die from accidental overdose.  The app will include user-interactive plots and graphs linking to different attributes of the people who lost their lives to the accidental overdose including their age, gender, and ethnicity and the number of drugs contributed to the death. Furthermore, it will offer users the options to explore the data from numerous perspectives including the distribution of number of deaths per month for years from 2012 to 2018. In addition, there will be a dynamic bar vertical plot to show the ranking for which drugs claimed the highest number of deaths during these years.
 
### Section 2:  Description of the data
**Accidental drug related deaths 2012-2018 data set (State of Connecticut)**

This data is provided by the local government of the state of Connecticut and was retrieved from [the State of Connecticut’s open data webpage](https://data.ct.gov/) through [US open data] (https://catalog.data.gov/dataset/accidental-drug-related-deaths-january-2012-sept-2015). 

The data was gathered from an investigation held by the Office of the Chief Medical Examiner and contains information extracted from scene investigations, death certificates and toxicity test performed to the victims.

**Content**

The dataset contains 5,105 reported accidental deaths caused by drug overdose in the state of Connecticut, from January 2012 to December 2018. From each observation, there is demographic information (such as `race`, `gender`, `age`, `place of residence`), information related to the scene investigation (`place of death`, `date of death`), and information about the results of the toxicity test for each of the drugs tested (`heroin`, `cocaine`, `fentanyl`, etc.). In addition, it contains the descriptions of the death as reported in the death certificate.

It is important to note that, for each drug examined during the toxicity test, there is a categorical variable that has Y if the drug tested positive, and NaN if not.


**Wrangling**

For the wrangling stage of the project, all the toxicity test results were casted into a binary variable in which 1 means that the drug tested positive in the toxicity test, and 0 if not. In addition, 25 observations were removed because the manner of death was reported as natural or it is still pending. NaNs from other variables were replaced with ‘No description’, in order to prevent from dropping valuable information.

### Section 3: Research questions and usage scenarios
#### The research question
What concerns us most is the people died from overdose. How should we describe them? Thus, we would like to raise the research question as:

*Who are the people who died the most from drug overdose?*

And we will answer these questions from several aspects: age, gender, ethnicity, and places people were found death.

#### Usage scenario
Mark is a social worker who helps drug addicts. He is interested in the location’s addicts were found dead. He wants to know what these people are more likely to be, so they could come up with better protective measures for them. For example, he notices some people still died even they were under care in the hospital. So, he would like to identify what these people are like, thus, in the future, they can pay more attention to them to prevent more deaths from drug overdose. When Mark logs on to the “Drug Overdose Observation App”, he could select the places people found death first. Then, he can explore several variables: age, gender, and ethnicity. By choosing one variable, he can see the distribution under this variable. So, Mark can take notes on what kind of people were died the most on one scenario. He can also choose variable combinations to see a combined result. During the investigation, Mark finds that Asian men aged from 50-55 were mostly died from drug overdose in the hospital. According to this result, he thinks they would need more medical care and looking after. Thus, he decides to call on more co-workers to pay attention to addicts who satisfy this description in the hospital.




*Reference[1]: GregRhee et al. (2019). Accidental drug overdose deaths in Connecticut, 2012–2018: The rise of polysubstance detection. Journal of Drug and Alcohol Dependence. Volume 205, 1 December 2019, 107671*
