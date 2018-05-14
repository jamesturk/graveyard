import React, { Component } from 'react';
import './App.css';

class InfoBlock extends Component {
  constructor() {
    super();
    this.layout = 'definition';
  }

  render() {
    if(this.layout === 'definition') {
      return this.renderAsDefinition();
    } else {
      return this.renderAsTable();
    }
  }

  renderAsDefinition() {
    const terms = this.data.map(
      (d, i) => <React.Fragment key={i}><dt>{d[0]}</dt><dd>{d[1]}</dd></React.Fragment>
    );
    return (
      <div className="block" id={this.id}>
        <h2>{this.title}</h2>
        <dl>
          {terms}
        </dl>
      </div>
    );
  }
}

class Cover extends InfoBlock {
  constructor() {
    super();
    this.id = 'cover';
    this.title = 'Cover';
    this.data = [
      ['Half Cover', '+2 to AC/Dex'],
      ['3/4 Cover', '+5 to AC/Dex'],
      ['Total Cover', 'Cannot be targeted'],
    ];
  }
}

class Conditions extends InfoBlock {
  constructor() {
    super();
    this.id = 'conditions';
    this.title = 'Conditions';
    this.data = [
      ["Blinded", 
       "Fails any check that requires sight. Attack rolls against have advantage, creature's attack roles have disadvantage."],
      ["Charmed", 
       "Can't attack or target charmer.  Charmer has advantage on social ability checks vs. creature."],
      ["Deafened", 
       "Fails any check that requires hearing."],
      ["Frightened", 
       "Disadvantage on ability checks &amp; attack roles when source of fear is within line of sight. Can't willingly move closer to source of fear."],
      ["Incapacitated", 
       "Can't take any actions or reactions."],
      ["Invisible", 
       "Impossible to see without aid of special sense. Creature does make noise, leave tracks. All attack rolls against creature have disadvantage, creature's attack rolls have advantage."],
      ["Paralyzed", 
       "Incapacitated &amp; can't move or speak. Fails all Str and Dex saving throws. Rolls against have advantage &amp; any attack that hits from within 5 ft is critical."],
      ["Petrified", 
        "Tranformed into stone, weight increased by ten.  Fails all Str and Dex saving throws. Rolls against have advantage.  Resistance to all damage &amp; immune to poison and disease."],
      ["Poison", 
       "Disadvantage on attack roles &amp; ability checks."],
      ["Prone", 
       "Can crawl at half-speed or spend half movement getting up.  Disadvantage on attack roles.  Attack rolls from within 5 feet have advantage, otherwise have disadvantage."],
      ["Restrained", 
       "Speed is zero.  Attack rolls have advantage, creatures attack has disadvantage.  Has disadvantage on Dex saving throws."],
      ["Stunned", 
       "Incapacitated, can't move, can speak only falteringly. Fails all Str and Dex saving throws.  Attack rolls against creature have advantage."],
      ["Unconscious", 
       "Incapacitated, can't move or speak.  Fails all Str and Dex saving throws. Attack rolls have advantage and all attacks that hit from within 5 feet are critical."],
    ];
  }
}

class SkillChecks extends InfoBlock {
  constructor() {
    super();
    this.id = "skill-checks";
    this.title = "Skill Checks";
    this.data = [
      ["Str", "Athletics"],
      ["Dex", "Acrobatics, Sleight of Hand, Stealth"],
      ["Con", "Concentration"],
      ["Int", "Arcana, History, Investigation, Nature, Religion"],
      ["Wis", "Animal Handling, Insight, Medicine, Perception, Survival"],
      ["Cha", "Deception, Intimidation, Performance, Persuasion"],
    ];
  }
}

class Actions extends InfoBlock {
  constructor() {
    super();
    this.id = 'actions';
    this.title = 'Actions';
    this.data = [
      ['Attack', ''],
      ['Cast a Spell', 'w/ casting time One Action. One spell per turn.'],
      ['Dash', 'Extra distance up to current speed.'],
      ['Disengage', "Movement won't provoke attacks of opportunity."],
      ['Dodge', 'Attacks against you have disadvantage.  Your Dex saving throws have advantage.'],
      ['Help', 'Lend aid to ally, giving it advantage on next turn.'],
      ['Hide', 'Make Dex (Stealth) check to hide.'],
      ['Ready', 'Prepare action to be used before next turn.  Can ready spell, item, attack.'],
      ['Search', 'Make appropriate Perception or Investigation check.'],
      ['Use Object', 'Potions, magic items, complex interactions.'],
    ];
  }
}

class Exhaustion extends InfoBlock {
  constructor() {
    super();
    this.id = 'exhaustion';
    this.title = 'Exhaustion';
    this.data = [
      [1, 'Disadvantage on ability checks'],
      [2, 'Speed halved'],
      [3, 'Disadvantage on attack roles & saving throws']
      [4, 'HP maximum halved'],
      [5, 'Speed reduced to zero'],
      [6, 'Death'],
    ];
    // note: long rest reduces exhaustion by 1
  }
}

class Lifestyle extends InfoBlock {
  constructor() {
    super();
    this.id = 'lifestyle';
    this.title = 'Lifestyle Expenses';
    this.data = [
       ["Wretched", "0"],
       ["Squalid", "1 sp"],
       ["Poor", "2 sp"],
       ["Modest", "1 gp"],
       ["Comfortable", "2 gp"],
       ["Wealthy", "4 sp"],
       ["Aristocratic", "10 gp+"],
    ];
  }
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <Actions />
      </div>
    );
  }
}

export default App;