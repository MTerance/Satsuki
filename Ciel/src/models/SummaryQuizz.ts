export interface SummaryQuizz {
    id: number;
    Name : string;
    Location?: LocationQuizz;
    GameType?: GameTypeQuizz;
    durationTime : number;
}

export interface GameTypeQuizz {
    id: number;
    Name: string;
    imgPath: string;
    tag: string;
}

export interface LocationQuizz {
    id:number;
    Name: string;
    imgPath: string;
}