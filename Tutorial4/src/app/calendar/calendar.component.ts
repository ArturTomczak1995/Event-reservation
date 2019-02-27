import { Component, OnInit } from '@angular/core';
import * as moment from 'moment';

@Component({
  selector: 'app-calendar',
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.css']
})
export class CalendarComponent implements OnInit {
  private monthName: string;
  private daysInCalendar: number;
  private firstDayOfMonth: number;
  private previousMonthDays: number;
  weeksInMonth = 6;
  weeksArr: any[][];
  dayName = moment.weekdays();
  private currentMonthDays: number;
  currentMonth = moment().format('MM');
  currentYear = moment().format('YYYY');


  pushToWeeksArr(minVal: number, maxVal: number, isCurrentMonth: boolean) {
    for (let i = minVal; i <= maxVal; i++) {
      const weeksArrLen = this.weeksArr.length - 1;
      this.weeksArr[weeksArrLen].push({i, isActive: isCurrentMonth});
      if (this.weeksArr[weeksArrLen].length % 7 === 0 && weeksArrLen !== this.weeksInMonth - 1) {
        this.weeksArr.push([]);
      }
    }
  }
  changeMonth(changeValue: number) {
    let monthBufor = Number(this.currentMonth) + changeValue;
    if (monthBufor ===  0) {
      monthBufor = 12;
      this.currentYear = (Number(this.currentYear) - 1).toString();
    }
    if (monthBufor === 13) {
      monthBufor = 1;
      this.currentYear = (Number(this.currentYear) + 1).toString();
    }
    console.log(this.currentYear);
    this.currentMonth = '0' + ( monthBufor ).toString();
    this.createCalendar();
  }

  changeYear(changeValue: number) {
    let yearBufor = Number(this.currentYear) + changeValue;
    if (yearBufor ===  0) { yearBufor = 12; }
    if (yearBufor === 13) { yearBufor = 1; }
    this.currentYear = ( yearBufor ).toString();
    this.createCalendar();
  }

  constructor() {

  }
  createCalendar() {
    this.currentMonthDays = moment(this.currentMonth + this.currentYear, 'MMYYYY').daysInMonth();
    this.monthName = moment.months()[Number(this.currentMonth) - 1];
    this.weeksArr = [[]];
    this.daysInCalendar = this.weeksInMonth * this.dayName.length;
    this.firstDayOfMonth = Number(moment('01' + this.currentMonth + this.currentYear, 'DDMMYYYY').format('d')) - 1;
    this.previousMonthDays = moment(this.currentMonth, 'MM').add(-1, 'month').daysInMonth();

    this.pushToWeeksArr(this.previousMonthDays - this.firstDayOfMonth, this.previousMonthDays, false);
    this.pushToWeeksArr(1, this.currentMonthDays, true);
    this.pushToWeeksArr(1, this.daysInCalendar - (this.currentMonthDays + this.firstDayOfMonth + 1), false);
  }


  ngOnInit() {
    this.createCalendar();
  }
}
