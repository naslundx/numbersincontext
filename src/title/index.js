import "./title.css"

const Title = () => {
    return (
        <header className="title transparentbox">
            <h1>Numbers in context</h1>
            <div>
                <p>What does <b>4.95 million people</b> or <b>510 000 km<sup>2</sup></b> really <i>mean</i>?</p>
                <p>It is much easier to understand <b>Half the population of London</b> or <b>Earth's total surface area</b>.</p>
            </div>
        </header>
    );
}

export default Title;