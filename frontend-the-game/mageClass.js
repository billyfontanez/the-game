class CharacterTypeMage{
    constructor(name, startingHp = 500, startingMp = 100, startingDefence = 30, klass = 'Mage', clain = 'Red Mage', abilities = {abilityOne: 'Fire Ball', abilityTwo: ' Basic Hit'}){
        this.name = name,
        this.klass = klass,
        this.clain = clain,
        this.startingHp = startingHp,
        this.startingMp = startingMp,
        this.startingDefence = startingDefence,
        this.abilities = abilities
    }

    renderStats(){
        console.log(`
Player Name: ${Object.values(this.name)}\n
Class: ${this.klass}\n
Clain: ${this.clain}\n
HP: ${this.startingHp}\n
MP: ${this.startingMp}\n
Defense: ${this.startingDefence}\n
Abilities: ${Object.values(this.abilities)}\n
        `)
      }
}

const wfontanez = new CharacterTypeMage({name:'Ice Wolf'});


const playerTwo = new CharacterTypeMage({name:'PlayerTwo'})
playerTwo.renderStats();