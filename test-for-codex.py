import streamlit as st


def visual_storyteller_html(story: str, typing_speed: int = 40) -> str:
    """Return embeddable HTML for the animated story viewer."""
    escaped = story.replace("`", "\`")
    return """
<div id='starfield'></div>
<div class='wrapper'>
  <h1 id='title'></h1>
  <div id='story'></div>
  <button id='restart'>Restart</button>
</div>
<style>
  body {{
    margin:0;
    background:linear-gradient(#000710,#040b20);
    color:#fff;
    font-family:Arial,Helvetica,sans-serif;
    height:100%;
    overflow:hidden;
  }}
  .wrapper {{
    position:relative;
    max-width:800px;
    margin:0 auto;
    padding:2rem;
    height:90vh;
    overflow-y:auto;
    text-align:center;
  }}
  #title {{
    font-size:2rem;
    margin-bottom:1rem;
    opacity:0;
    animation:fadeIn 2s forwards;
    text-shadow:0 0 8px #89b4fa;
  }}
  .sentence {{
    margin:1rem 0;
    font-size:1.2rem;
    text-shadow:0 0 6px #89b4fa;
  }}
  #restart {{
    margin-top:1rem;
    padding:0.5rem 1.2rem;
    background:#111;
    border:none;
    color:#fff;
    border-radius:6px;
    cursor:pointer;
  }}
  #starfield {{
    position:fixed;
    top:0;left:0;width:100%;height:100%;
    z-index:-1;
    overflow:hidden;
  }}
  .star {{
    position:absolute;
    bottom:-2px;
    width:2px;height:2px;
    background:rgba(255,255,255,0.8);
    border-radius:50%;
    animation:float linear infinite;
  }}
  @keyframes float {{
    from {{transform:translateY(0)}}
    to {{transform:translateY(-110vh)}}
  }}
  @keyframes fadeIn {{
    to {{opacity:1}}
  }}
</style>
<script>
const story = `{escaped}`;
const [titleText, ...rest] = story.trim().split(/\n+/);
const sentences = rest.join(' ').split(/(?<=[.!?])\s+/).filter(Boolean);
const titleEl = document.getElementById('title');
const storyEl = document.getElementById('story');
const speed = {typing_speed};
function createStars(n){
  const field=document.getElementById('starfield');
  field.innerHTML='';
  for(let i=0;i<n;i++){{
    const s=document.createElement('div');
    s.className='star';
    s.style.left=Math.random()*100+'%';
    s.style.animationDuration=20+Math.random()*40+'s';
    s.style.animationDelay=-Math.random()*60+'s';
    field.appendChild(s);
  }}
}
function sleep(ms){{return new Promise(r=>setTimeout(r,ms))}}
async function typeSentence(text){{
  const p=document.createElement('p');
  p.className='sentence';
  storyEl.appendChild(p);
  for(let i=0;i<text.length;i++){{
    p.textContent+=text.charAt(i);
    storyEl.scrollTop=storyEl.scrollHeight;
    await sleep(speed);
  }}
  await sleep(500);
}}
async function play(){{
  storyEl.innerHTML='';
  titleEl.textContent=titleText;
  await sleep(500);
  for(const s of sentences){{
    await typeSentence(s);
  }}
}}
document.getElementById('restart').addEventListener('click',play);
createStars(80);
play();
</script>
""".format(escaped=escaped, typing_speed=typing_speed)


st.title("Visual Storyteller")
user_story = st.text_area(
    "Enter a story (first line is the title)",
    "The Enchanted Forest\nStars shimmered above the quiet trees. A soft wind whispered secrets. Magic lingered in every shadow."
)
html_code = visual_storyteller_html(user_story)
st.components.v1.html(html_code, height=600, scrolling=True)
