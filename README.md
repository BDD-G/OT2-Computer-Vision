# Automated Quality Control in Life Science Laboratories

This repository comprises the source code for a sophisticated system that streamlines the quality control process in life science laboratories. Bioengineering plays a pivotal role in modern-day society, ranging from the development of genetically modified plants to the production of advanced life-saving drugs. However, there is still ample scope for making bioengineering processes more automated and sustainable.

## Overview

Our system employs the Opentrons OT-2, an economical industrial liquid handling robot, to automate quality control processes. This project represents a continuation of a prior master's thesis, which addressed limitations associated with processing delays and real-time communication with the robot. We have integrated vision-based artificial intelligence into our system to monitor the robotic arm, detect attached tips, measure liquid presence inside tips, and provide real-time feedback to ensure accurate operations. In the event of any issues, such as missing tips or insufficient liquid, our system can promptly interrupt the process.

## Solution Flow

This system involves using an OT-2 robot with a Raspberry Pi computer. A camera sends pictures to a PC, which checks them and sends data to the Raspberry Pi. The Raspberry Pi uses this data to control the robot arm, which sends data back to the PC for quality checks. Detailed logs are generated at the end of each operation. The PC and Raspberry Pi use parallel computing to work together in a server-client setup for efficiency.

<p align="center">
  <img src="https://i.imgur.com/67VGjJK.png" alt="System Flowchart" width="50%" height="50%">
  <br>
  <em>System Flowchart: Overview of the Proposed Solution</em>
</p>






## Results

Our system accurately detects tips, liquids, and liquid levels, even with small volumes. We fine-tuned machine learning models to improve accuracy while avoiding overfitting. The model performs exceptionally well, balancing precision and recall, which is crucial for real-world applications. Additionally, our system accurately measures liquid levels, with the potential for further improvements using advanced cameras or the Segment Anything model.
<p align="center">
  <img src="https://i.imgur.com/lxZENRv.png" alt="Object Detection Model Evaluations" width="50%" height="50%">
  <br>
  <em>Object Detection Model Evaluations</em>
</p>

<br> <!-- Empty line for vertical spacing -->

<p align="center">
  <img src="https://i.imgur.com/vhCxIBQ.png" alt="12x8 Greiner 96 well plate" width="20%" height="20%">
  <img src="https://i.imgur.com/vVE1kak.png" alt="Output Logs" width="55%" height="55%">
</p>
<p align="center">
  <em>12x8 Greiner 96 well plate: It can be seen from the alignment of plate with the output logs that there is no liquid at positions where the system detected it 'MISSING' in image 2. A red circle highlights empty positions.</em>
</p>





## Conclusion

Our project has successfully achieved its goals of enhancing automation in life science laboratories, reducing processing time, and ensuring accuracy in operations. It is aligned with the United Nations Sustainable Development Goals, especially SDGs 9 and 12, by promoting sustainable infrastructure and responsible consumption and production. Our system makes lab automation more accessible, efficient, and reliable, thus benefiting scientific research worldwide. We are confident that our contribution will significantly impact the field of life sciences, and we are committed to further improving our system to meet the evolving needs of the scientific community.
